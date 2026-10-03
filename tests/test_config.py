from app.config import settings


def test_openai_configuration_loaded():
    assert settings.openai_api_key
    assert settings.openai_model