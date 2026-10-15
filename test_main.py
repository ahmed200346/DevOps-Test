from model_pipeline import prepare_data

def test_prepare_data_returns_four_elements():
    result = prepare_data('Churn_Modelling.csv')
    assert len(result) == 4
