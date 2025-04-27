"""
Core Backtesting Engine
- Handles filtering, weighting, and optimization.
- Designed to maximize Dᵀw manually within specified bounds without external solvers.
- Optimized for memory efficiency, modularity, and extensibility.
"""

import time
import pandas as pd
import logging

from app.utils import get_revision_dates, apply_top_n_filter, apply_value_threshold_filter
from app.data_loader import load_data_field

# ------------------------------------------------------------------------------

def compute_optimized_weights(values: pd.Series, lb: float, ub: float) -> dict:
    """
    Compute optimized weights manually without using a solver.
    
    Strategy:
    - Assign lower bound weight to all securities first.
    - Distribute leftover weight preferentially to higher-valued securities.
    - Ensure each security remains within [lb, ub] bounds.
    - Guarantee total weights sum exactly to 1.

    Args:
        values (pd.Series): Series of security values (e.g., market capitalization).
        lb (float): Lower bound for individual weights.
        ub (float): Upper bound for individual weights.

    Returns:
        dict: Mapping of security identifiers to their assigned weights.
    """
    if values.empty:
        return {}

    n = len(values)
    sorted_vals = values.sort_values(ascending=False)
    
    # Step 1: Assign minimum weight to all securities
    weights = {sec: lb for sec in sorted_vals.index}
    total_assigned = lb * n

    # Step 2: Calculate remaining weight to distribute
    leftover_weight = 1.0 - total_assigned

    # Step 3: Distribute leftover weight to highest value securities
    for sec in sorted_vals.index:
        max_additional = ub - lb  # Maximum extra weight security can take
        add_weight = min(max_additional, leftover_weight)
        weights[sec] += round(add_weight, 6)
        leftover_weight -= add_weight

        if leftover_weight <= 0:
            break

    return weights

# ------------------------------------------------------------------------------

def run_backtest(request: dict) -> dict:
    """
    Execute the backtest based on given request parameters.

    Workflow:
    - Load data field (e.g., market cap, volume) from dataset.
    - Generate rebalancing dates according to calendar rule.
    - For each date:
        - Apply filtering strategy (Top-N or Value Threshold).
        - Apply weighting strategy (Equal or Optimized).
        - Store resulting weights if successful.
    - Return execution time and final weights.

    Args:
        request (dict): Dictionary containing dataset path, calendar rules, 
                        filter settings, and weighting settings.

    Returns:
        dict: Dictionary containing execution time and calculated weights per date.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    start = time.time()

    # Step 1: Load dataset
    logging.info("Loading data field: %s", request['filter']['data_field'])
    df = load_data_field(request['dataset_path'], request['filter']['data_field'])

    # Step 2: Get revision dates (custom or quarterly)
    revision_dates = get_revision_dates(request['calendar'])
    logging.info("Revision Dates generated: %s", revision_dates)

    weights_result = {}

    # Step 3: Process each rebalancing date
    for date in revision_dates:
        try:
            date_obj = pd.to_datetime(date).date()
            date_index = df.index.date

            # Check if date exists in the dataset
            if date_obj not in date_index:
                logging.warning("Date %s not found in data index, skipping.", date)
                continue

            # Extract the row corresponding to the rebalancing date
            row = df.loc[df.index.date == date_obj].squeeze()

            ### Filtering Step ###
            if request['filter']['filter_type'] == 'top_n':
                filtered = apply_top_n_filter(row, request['filter']['N'])
                logging.info("Filter Type: Top N | Securities selected: %d", len(filtered))
            elif request['filter']['filter_type'] == 'value_threshold':
                filtered = apply_value_threshold_filter(row, request['filter']['P'])
                logging.info("Filter Type: Value Threshold | Securities selected: %d", len(filtered))
            else:
                raise ValueError("Invalid filter type specified in request.")

            if filtered.empty:
                logging.warning("Filtered securities empty after applying filter. Skipping date: %s", date)
                continue

            ### Weighting Step ###
            if request['weighting']['method'] == 'equal':
                n = len(filtered)
                weights = {sec: round(1/n, 6) for sec in filtered.index}
                logging.info("Equal Weighting applied | Total Securities: %d", n)

            elif request['weighting']['method'] == 'optimized':
                vals = filtered
                lb = request['weighting']['lb']
                ub = request['weighting']['ub']
                weights = compute_optimized_weights(vals, lb, ub)
                logging.info("Optimized Weighting applied | Securities after optimization: %d", len(weights))

            # If no weights could be assigned, skip this date
            if not weights:
                logging.warning("Weights empty after weighting. Skipping date: %s", date)
                continue

            weights_result[date] = weights

        except Exception as e:
            logging.error("Error processing date %s: %s", date, str(e))
            continue

    end = time.time()
    total_time = round(end - start, 4)

    logging.info("Backtest completed. Execution time: %s seconds", total_time)

    # Convert date keys to string format for JSON serialization
    weights_result_str_keys = {str(k): v for k, v in weights_result.items()}

    return {
        "execution_time": total_time,
        "weights": weights_result_str_keys
    }