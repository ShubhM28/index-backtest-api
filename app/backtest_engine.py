import time
import pandas as pd
from app.utils import get_revision_dates, apply_top_n_filter, apply_value_threshold_filter
from app.data_loader import load_data_field

def compute_optimized_weights(values: pd.Series, lb: float, ub: float) -> dict:
    if values.empty:
        return {}
    
    normed_vals = values / values.sum()
    clipped = normed_vals.clip(lower=lb, upper=ub)
    total = clipped.sum()
    if total == 0:
        return {}

    final_weights = clipped / total
    return final_weights.round(6).to_dict()

def run_backtest(request: dict) -> dict:
    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    start = time.time()

    # Load field
    logging.info("Loading data field: %s", request['filter']['data_field'])
    df = load_data_field(request['dataset_path'], request['filter']['data_field'])
    revision_dates = get_revision_dates(request['calendar'])

    weights_result = {}

    logging.info("Revision Dates generated: %s", revision_dates)

    for date in revision_dates:
        try:
            date_index = df.index.date

            if date not in date_index:
                logging.warning("Date %s not found in data index, skipping.", date)
                continue

            row = df.loc[df.index.date == date].squeeze()

            ### Filtering ###
            if request['filter']['filter_type'] == 'top_n':
                filtered = apply_top_n_filter(row, request['filter']['N'])
                logging.info("Filter Type: Top N | Securities selected: %d", len(filtered))
            elif request['filter']['filter_type'] == 'value_threshold':
                filtered = apply_value_threshold_filter(row, request['filter']['P'])
                logging.info("Filter Type: Value Threshold | Securities selected: %d", len(filtered))
            else:
                raise ValueError("Invalid filter type")

            if filtered.empty:
                logging.warning("Filtered securities empty after applying filter. Skipping date: %s", date)
                continue

            ### Weighting ###
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

    weights_result_str_keys = {str(k): v for k, v in weights_result.items()}

    return {
        "execution_time": round(end - start, 4),
        "weights": weights_result_str_keys
    }