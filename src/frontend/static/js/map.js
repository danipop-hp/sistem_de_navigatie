const centruHarta = JSON.parse(document.body.dataset.centruHarta);
const traseuInitial = JSON.parse(document.body.dataset.traseuInitial);
const serviciuRutareActiv = JSON.parse(document.body.dataset.serviciuRutareActiv);

let punctStart = null;
let punctFinal = null;
let markerStart = null;
let markerFinal = null;
let traseuLayer = null;
let ruteIstoric = [];

const statusEl = document.getElementById("status");
const distantaEl = document.getElementById("distantaCurenta");
const durataEl = document.getElementById("durataCurenta");
const numarRuteEl = document.getElementById("numarRute");
const listaIstoricEl = document.getElementById("listaIstoric");
const badgeRutareEl = document.getElementById("badgeRutare");

const map = L.map("map").setView(centruHarta, 16);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

function actualizeazaStatus(text) {
    statusEl.textContent = text;
}

function afiseazaMetrici(distantaM = null, durataMin = null) {
    distantaEl.textContent = distantaM === null ? "-" : `${distantaM.toFixed(0)} m`;
    durataEl.textContent = durataMin === null ? "-" : `${durataMin.toFixed(1)} min`;
}

function randText(value, fallback = "-") {
    return value === null || value === undefined || value === "" ? fallback : String(value);
}

function reseteazaSelectia() {
    punctStart = null;
    punctFinal = null;

    if (markerStart) {
        map.removeLayer(markerStart);
        markerStart = null;
    }
    if (markerFinal) {
        map.removeLayer(markerFinal);
        markerFinal = null;
    }
    if (traseuLayer) {
        map.removeLayer(traseuLayer);
        traseuLayer = null;
    }

    afiseazaMetrici();
    actualizeazaStatus("Click 1: Start, Click 2: Destinatie, Click 3: Reset. Ruta este calculata pe reteaua rutiera.");
}

function deseneazaRutaPeHarta(pathGps, fitBounds = true) {
    if (!Array.isArray(pathGps) || pathGps.length < 2) {
        return;
    }

    if (traseuLayer) {
        map.removeLayer(traseuLayer);
    }

    traseuLayer = L.polyline(pathGps, {
        color: "#dc2f02",
        weight: 6,
        opacity: 0.85
    }).addTo(map);

    if (fitBounds) {
        map.fitBounds(traseuLayer.getBounds(), { padding: [20, 20] });
    }
}

async function incarcaIstoric() {
    try {
        const raspuns = await fetch("/istoric_rute?limita=12");
        const date = await raspuns.json();

        if (!raspuns.ok || date.status !== "success") {
            throw new Error(date.mesaj || "Nu s-a putut incarca istoricul.");
        }

        ruteIstoric = Array.isArray(date.rute) ? date.rute : [];
        numarRuteEl.textContent = String(date.count || ruteIstoric.length);
        randareListaIstoric();
    } catch (eroare) {
        listaIstoricEl.innerHTML = "<li>Istoricul nu a putut fi incarcat.</li>";
        numarRuteEl.textContent = "-";
    }
}

function randareListaIstoric() {
    listaIstoricEl.innerHTML = "";

    if (!ruteIstoric.length) {
        listaIstoricEl.innerHTML = "<li>Nu exista rute salvate inca.</li>";
        return;
    }

    for (const ruta of ruteIstoric) {
        const item = document.createElement("li");

        const distanta = ruta.distanta_m === null ? "-" : `${Number(ruta.distanta_m).toFixed(0)} m`;
        const durata = ruta.durata_min === null ? "-" : `${Number(ruta.durata_min).toFixed(1)} min`;

        item.innerHTML = `
            <div><strong>${randText(ruta.traseu_complet, "Ruta")}</strong></div>
            <div class="meta">Distanta: ${distanta} | Durata: ${durata}</div>
            <div class="meta">Data: ${randText(ruta.data_ora, "-")}</div>
            <div class="actiuni-istoric"></div>
        `;

        const containerButon = item.querySelector(".actiuni-istoric");
        const buton = document.createElement("button");
        buton.type = "button";
        buton.textContent = "Afiseaza pe harta";
        buton.addEventListener("click", () => {
            deseneazaRutaPeHarta(ruta.path_gps || []);
            afiseazaMetrici(
                typeof ruta.distanta_m === "number" ? ruta.distanta_m : null,
                typeof ruta.durata_min === "number" ? ruta.durata_min : null
            );
            actualizeazaStatus("Ruta din istoric a fost afisata pe harta.");
        });
        containerButon.appendChild(buton);

        listaIstoricEl.appendChild(item);
    }
}

async function cereRuta() {
    const raspuns = await fetch("/calculeaza-ruta-harta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start: punctStart, end: punctFinal })
    });

    const date = await raspuns.json();
    if (!raspuns.ok) {
        throw new Error(date.message || "Nu s-a putut calcula ruta.");
    }

    deseneazaRutaPeHarta(date.path_gps);
    afiseazaMetrici(date.distance_m, date.duration_min);

    await fetch("/salveaza_ruta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            path_gps: date.path_gps,
            distance_m: date.distance_m,
            duration_min: date.duration_min,
            tip_ruta: "osm_astar"
        })
    });

    await incarcaIstoric();

    actualizeazaStatus(`Ruta calculata cu A*: ${date.distance_m} m, ~${date.duration_min} min. Click inca o data pe harta pentru reset.`);
}

map.on("click", async (event) => {
    if (!serviciuRutareActiv) {
        alert("Serviciul de rutare nu este activ. Verifica dependintele backend.");
        return;
    }

    const lat = event.latlng.lat;
    const lon = event.latlng.lng;

    if (!punctStart) {
        punctStart = { lat, lon };
        markerStart = L.marker([lat, lon]).addTo(map).bindPopup("Start").openPopup();
        actualizeazaStatus("Start setat. Alege acum destinatia pe un drum.");
        return;
    }

    if (!punctFinal) {
        punctFinal = { lat, lon };
        markerFinal = L.marker([lat, lon]).addTo(map).bindPopup("Destinatie");
        try {
            await cereRuta();
        } catch (eroare) {
            alert(eroare.message);
            punctFinal = null;
            if (markerFinal) {
                map.removeLayer(markerFinal);
                markerFinal = null;
            }
        }
        return;
    }

    reseteazaSelectia();
});

if (Array.isArray(traseuInitial) && traseuInitial.length >= 2) {
    deseneazaRutaPeHarta(traseuInitial);
}

if (!serviciuRutareActiv) {
    badgeRutareEl.textContent = "Serviciu inactiv";
    badgeRutareEl.classList.add("inactiv");
    actualizeazaStatus("Serviciul de rutare nu este activ. Instaleaza dependintele si ruleaza aplicatia cu internet la prima pornire.");
}

document.getElementById("resetBtn").addEventListener("click", reseteazaSelectia);
document.getElementById("incarcaIstoricBtn").addEventListener("click", incarcaIstoric);
incarcaIstoric();
