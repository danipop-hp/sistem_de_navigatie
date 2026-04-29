from pathlib import Path

import pytest

from src.backend import app as modul_app


@pytest.fixture()
def client_test(tmp_path):
	cale_baza_teste = tmp_path / "navigatie_test.db"
	modul_app.CALE_BAZA_DATE = Path(cale_baza_teste)
	modul_app.init_db()
	modul_app.app.config["TESTING"] = True

	with modul_app.app.test_client() as client:
		yield client


def test_map_este_disponibila(client_test):
	raspuns = client_test.get("/map")

	assert raspuns.status_code == 200
	assert b"Sistem de Navigatie Urbana" in raspuns.data


def test_calculeaza_ruta_valida(monkeypatch, client_test):
	def ruta_falsa(lat_start, lon_start, lat_final, lon_final):
		return [[lat_start, lon_start], [lat_final, lon_final]], 1200.0, 3.2

	monkeypatch.setattr(modul_app, "calculeaza_ruta_osm", ruta_falsa)

	raspuns = client_test.post(
		"/calculeaza-ruta-harta",
		json={
			"start": {"lat": 47.66, "lon": 23.57},
			"end": {"lat": 47.67, "lon": 23.58},
		},
	)

	date = raspuns.get_json()
	assert raspuns.status_code == 200
	assert date["status"] == "success"
	assert date["distance_m"] == pytest.approx(1200.0)
	assert date["algorithm"] == "astar"



def test_calculeaza_ruta_ignora_algorithm_din_payload(monkeypatch, client_test):
	def ruta_falsa(lat_start, lon_start, lat_final, lon_final):
		return [[lat_start, lon_start], [lat_final, lon_final]], 900.0, 2.4

	monkeypatch.setattr(modul_app, "calculeaza_ruta_osm", ruta_falsa)

	raspuns = client_test.post(
		"/calculeaza-ruta-harta",
		json={
			"start": {"lat": 47.66, "lon": 23.57},
			"end": {"lat": 47.67, "lon": 23.58},
			"algorithm": "algo-inexistent",
		},
	)

	date = raspuns.get_json()
	assert raspuns.status_code == 200
	assert date["status"] == "success"
	assert date["algorithm"] == "astar"


def test_calculeaza_ruta_coord_invalide(client_test):
	raspuns = client_test.post(
		"/calculeaza-ruta-harta",
		json={
			"start": {"lat": "abc", "lon": 23.57},
			"end": {"lat": 47.67, "lon": 23.58},
		},
	)

	assert raspuns.status_code == 400
	assert raspuns.get_json()["status"] == "error"


def test_salveaza_ruta_si_citeste_istoric(client_test):
	payload = {
		"path_gps": [[47.66, 23.57], [47.67, 23.58]],
		"distance_m": 1450.5,
		"duration_min": 4.1,
	}

	raspuns_salveaza = client_test.post("/salveaza_ruta", json=payload)
	assert raspuns_salveaza.status_code == 200
	assert raspuns_salveaza.get_json()["status"] == "success"

	raspuns_istoric = client_test.get("/istoric_rute?limita=5")
	date_istoric = raspuns_istoric.get_json()

	assert raspuns_istoric.status_code == 200
	assert date_istoric["status"] == "success"
	assert date_istoric["count"] >= 1
	assert len(date_istoric["rute"]) >= 1


def test_salveaza_ruta_respinge_distance_invalid(client_test):
	payload = {
		"path_gps": [[47.66, 23.57], [47.67, 23.58]],
		"distance_m": "nu_este_numar",
		"duration_min": 4.1,
	}

	raspuns = client_test.post("/salveaza_ruta", json=payload)

	assert raspuns.status_code == 400
	assert raspuns.get_json()["status"] == "error"
