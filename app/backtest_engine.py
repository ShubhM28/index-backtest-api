import time
from app.utils import get_revision_dates, apply_top_n_filter, apply_value_threshold_filter
from app.data_loader import load_data_field

def run_backtest(request: dict) -> dict:
    start = time.time()

    # Load field
    df = load_data_field(request['dataset_path'], request['filter']['data_field'])
    revision_dates = get_revision_dates(request['calendar'])

    weights_result = {}

    for date in revision_dates:
        try:
            row = df.loc[date]

            ### Filtering ###
            if request['filter']['filter_type'] == 'top_n':
                filtered = apply_top_n_filter(row, request['filter']['N'])
            elif request['filter']['filter_type'] == 'value_threshold':
                filtered = apply_value_threshold_filter(row, request['filter']['P'])
            else:
                raise ValueError("Invalid filter type")

            if filtered.empty:
                continue

            ### Weighting ###
            if request['weighting']['method'] == 'equal':
                n = len(filtered)
                weights = {sec: round(1/n, 4) for sec in filtered.index}
            elif request['weighting']['method'] == 'optimized':
                vals = filtered
                lb = request['weighting']['lb']
                ub = request['weighting']['ub']
                total = vals.sum()
                raw_weights = vals / total
                clipped = raw_weights.clip(lower=lb, upper=ub)
                normalized = clipped / clipped.sum()
                weights = normalized.round(4).to_dict()

            weights_result[date] = weights

        except KeyError:
            continue

    end = time.time()
    return {
        "execution_time": round(end - start, 4),
        "weights": weights_result
    }