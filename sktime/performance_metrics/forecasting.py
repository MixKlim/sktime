import numpy as np
from sktime.utils.validation.forecasting import check_consistent_time_indices, validate_obs_horizon

__author__ = ['Markus Löning']
__all__ = ["mase_score", "smape_score"]

# for reference implementations, see https://github.com/M4Competition/M4-methods/blob/master/ML_benchmarks.py


def mase_score(y_true, y_pred, y_train, sp=1):
    """Negative mean absolute scaled error

    Parameters
    ----------
    y_true : pandas Series of shape = (fh,) where fh is the forecasting horizon
        Ground truth (correct) target values.
    y_pred : pandas Series of shape = (fh,)
        Estimated target values.
    y_train : pandas Series of shape = (n_obs,)
        Observed training values.
    sp : int
        Seasonal periodicity of training data.

    Returns
    -------
    loss : float
        MASE loss

    References
    ----------
    ..[1]   Hyndman, R. J. (2006). "Another look at measures of forecast accuracy", Foresight, Issue 4.
    """
    check_consistent_time_indices(y_true, y_pred)

    # check if training series is before forecasted series
    train_index = validate_obs_horizon(y_train.index)
    pred_index = validate_obs_horizon(y_pred)
    if train_index.max() >= pred_index.min():
        raise ValueError(f"Found y_train with time index which is not "
                         f"before time index of y_pred")

    #  naive seasonal prediction
    y_train = np.asarray(y_train)
    y_pred_naive = y_train[:-sp]

    # mean absolute error of naive seasonal prediction
    mae_naive = np.mean(np.abs(y_train[sp:] - y_pred_naive))

    return -np.mean(np.abs(y_true - y_pred)) / mae_naive


def smape_score(y_true, y_pred):
    """Negative symmetric mean absolute percentage error

    Parameters
    ----------
    y_true : pandas Series of shape = (fh,) where fh is the forecasting horizon
        Ground truth (correct) target values.
    y_pred : pandas Series of shape = (fh,)
        Estimated target values.

    Returns
    -------
    loss : float
        SMAPE loss
    """
    check_consistent_time_indices(y_true, y_pred)

    nominator = np.abs(y_true - y_pred)
    denominator = np.abs(y_true) + np.abs(y_pred)
    return -2 * np.mean(nominator / denominator)
