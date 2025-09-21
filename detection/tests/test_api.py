import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from detection.models import State, NewsCheck

pytestmark = pytest.mark.django_db

client = APIClient()

def test_health_check():
    url = reverse("health_check")
    res = client.get(url)
    assert res.status_code == 200
    assert res.json()["status"] == "OK"


def test_check_news_creates_record():
    # seed state
    kerala = State.objects.create(name="Kerala")

    url = reverse("check_news")
    payload = {"text": "Kerala CM announced free laptops", "location": "Kerala"}
    res = client.post(url, payload, format="json")

    assert res.status_code == 200
    data = res.json()

    # response keys
    assert "prediction" in data
    assert "sources" in data
    assert "education" in data

    # DB record created
    assert NewsCheck.objects.filter(state=kerala).exists()


def test_map_data_returns_state_summary():
    state = State.objects.create(name="Tamil Nadu")
    NewsCheck.objects.create(
        state=state,
        text="Some fake claim",
        text_en="Some fake claim",
        prediction_label="Fake",
        confidence=0.95,
    )

    url = reverse("map_data")
    res = client.get(url)
    assert res.status_code == 200
    data = res.json()

    assert state.name in data
    assert "fake" in data[state.name]
    assert "status" in data[state.name]


def test_state_news_returns_items():
    state = State.objects.create(name="Karnataka")
    NewsCheck.objects.create(
        state=state,
        text="Kannada fake claim",
        text_en="Kannada fake claim",
        prediction_label="Fake",
        confidence=0.88,
    )

    url = reverse("state_news", args=[state.name])
    res = client.get(url)
    assert res.status_code == 200
    data = res.json()

    assert data["state"] == state.name
    assert "fake_news" in data
    assert len(data["fake_news"]) >= 1
