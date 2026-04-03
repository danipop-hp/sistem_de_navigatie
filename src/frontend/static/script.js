const grila = document.getElementById("grid");
const randuri = 5;
const coloane = 5;
const celule = [];
const hartaOras = [
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0]
];
const INTARZIERE_VIZITA_MS = 120;
let idRulareAnimatie = 0;
let punctStart = null;
let punctSfarsit = null;

function trimiteDrumLaHarta(celuleDrum) {
    return fetch('/proiecteaza-harta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: celuleDrum })
    }).then((response) => {
        if (!response.ok) {
            throw new Error('Serverul nu a putut proiecta drumul pe harta.');
        }
        return fetch('/salveaza_ruta', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ puncte: celuleDrum })
        });
    }).then((responseSalvare) => {
        if (!responseSalvare.ok) {
            console.warn('Ruta a fost proiectata, dar salvarea in istoric a esuat.');
        }
        window.location.href = '/map';
    });
}

function setMode(modNou){
    console.info(`Modul ${modNou} nu mai este folosit. Selecteaza direct pe harta: start, destinatie, apoi reset.`);
}

function handleCellClick(rand, coloana) {
    if (hartaOras[rand][coloana] === 0) {
        alert("Nu poti pune puncte pe cladiri! Selecteaza o strada.");
        return;
    }

    const celula = celule[rand][coloana];

    if (!punctStart) {
        punctStart = [rand, coloana];
        celula.classList.remove("path", "visited");
        celula.classList.add("start");
        return;
    }

    if (!punctSfarsit) {
        if (punctStart[0] === rand && punctStart[1] === coloana) {
            alert("Destinatia trebuie sa fie diferita de start.");
            return;
        }

        punctSfarsit = [rand, coloana];
        celula.classList.remove("path", "visited");
        celula.classList.add("end");
        ruleazaNavigatia();
        return;
    }

    resetareHarta();
}

function resetareHarta() {
    idRulareAnimatie += 1;
    punctStart = null;
    punctSfarsit = null;

    for (let i = 0; i < randuri; i++) {
        for (let j = 0; j < coloane; j++) {
            const celula = celule[i][j];
            celula.classList.remove("start", "end", "path", "visited", "obstacle");
            if (hartaOras[i][j] === 0) {
                celula.classList.add("obstacle");
            }
        }
    }
}

for(let i=0;i<randuri;i++){
    celule[i]=[];
    for(let j=0;j<coloane;j++){
        const celula = document.createElement("div");
        celula.classList.add("cell");

        if(hartaOras[i][j] === 0) {
            celula.classList.add("obstacle");
        } else {
            celula.addEventListener("click", () => handleCellClick(i, j));
        }

        grila.appendChild(celula);
        celule[i][j]=celula;
    }
}

function ruleazaNavigatia(){
    if(!punctStart || !punctSfarsit){
        alert("Selecteaza mai intai startul si destinatia.");
        return;
    }

    idRulareAnimatie += 1;
    const idRulare = idRulareAnimatie;

    document.querySelectorAll(".path").forEach(c=>c.classList.remove("path"));
    document.querySelectorAll(".visited").forEach(c=>c.classList.remove("visited"));
    const pozitieStart = punctStart;
    const pozitieFinal = punctSfarsit;

    const setDeschis = [pozitieStart];
    const precedent = Array.from({length:randuri},()=>Array(coloane).fill(null));
    const scorG = Array.from({length:randuri},()=>Array(coloane).fill(Infinity));
    const scorF = Array.from({length:randuri},()=>Array(coloane).fill(Infinity));
    const directii=[[0,1],[1,0],[0,-1],[-1,0]];
    const ordineVizitare = [];

    const euristica = (x,y) => Math.abs(x - pozitieFinal[0]) + Math.abs(y - pozitieFinal[1]);

    scorG[pozitieStart[0]][pozitieStart[1]] = 0;
    scorF[pozitieStart[0]][pozitieStart[1]] = euristica(pozitieStart[0], pozitieStart[1]);

    while(setDeschis.length){
        let indexOptim = 0;
        for(let i=1;i<setDeschis.length;i++){
            const [cx,cy] = setDeschis[i];
            const [bx,by] = setDeschis[indexOptim];
            if(scorF[cx][cy] < scorF[bx][by]) indexOptim = i;
        }

        const [x,y] = setDeschis.splice(indexOptim,1)[0];
        ordineVizitare.push([x,y]);
        if(x===pozitieFinal[0] && y===pozitieFinal[1]) break;

        for(const [dx,dy] of directii){
            const nx=x+dx, ny=y+dy;
            if(nx<0 || nx>=randuri || ny<0 || ny>=coloane) continue;
            if(hartaOras[nx][ny] !== 1) continue;

            const scorGTemporar = scorG[x][y] + 1;
            if(scorGTemporar < scorG[nx][ny]){
                precedent[nx][ny]=[x,y];
                scorG[nx][ny]=scorGTemporar;
                scorF[nx][ny]=scorGTemporar + euristica(nx, ny);

                if(!setDeschis.some(([ox,oy]) => ox===nx && oy===ny)){
                    setDeschis.push([nx,ny]);
                }
            }
        }
    }

    if(pozitieStart[0]!==pozitieFinal[0] || pozitieStart[1]!==pozitieFinal[1]){
        if(precedent[pozitieFinal[0]][pozitieFinal[1]]===null){
            ordineVizitare.forEach(([vx, vy], index) => {
                setTimeout(() => {
                    if(idRulare !== idRulareAnimatie) return;
                    const celula = celule[vx][vy];
                    if(!celula.classList.contains("start") && !celula.classList.contains("end")){
                        celula.classList.add("visited");
                    }
                }, index * INTARZIERE_VIZITA_MS);
            });

            setTimeout(() => {
                if(idRulare !== idRulareAnimatie) return;
                alert("Nu există drum disponibil!");
            }, ordineVizitare.length * INTARZIERE_VIZITA_MS);
            return;
        }
    }

    const celuleDrum = [];
    let pozitieDrum=pozitieFinal;
    while(pozitieDrum && (pozitieDrum[0]!==pozitieStart[0] || pozitieDrum[1]!==pozitieStart[1])){
        const [x,y]=pozitieDrum;
        if(!celule[x][y].classList.contains("end")) celuleDrum.push([x,y]);
        pozitieDrum=precedent[x][y];
    }

    ordineVizitare.forEach(([vx, vy], index) => {
        setTimeout(() => {
            if(idRulare !== idRulareAnimatie) return;
            const celula = celule[vx][vy];
            if(!celula.classList.contains("start") && !celula.classList.contains("end")){
                celula.classList.add("visited");
            }
        }, index * INTARZIERE_VIZITA_MS);
    });

    const intarziereStartDrum = ordineVizitare.length * INTARZIERE_VIZITA_MS;
    celuleDrum.reverse().forEach(([px, py], index) => {
        setTimeout(() => {
            if(idRulare !== idRulareAnimatie) return;
            const celula = celule[px][py];
            celula.classList.remove("visited");
            celula.classList.add("path");
        }, intarziereStartDrum + index * INTARZIERE_VIZITA_MS);
    });

    const drumComplet = (pozitieStart[0] === pozitieFinal[0] && pozitieStart[1] === pozitieFinal[1])
        ? [pozitieStart]
        : [pozitieStart, ...celuleDrum, pozitieFinal];

    const intarziereProiectie = intarziereStartDrum + (celuleDrum.length * INTARZIERE_VIZITA_MS) + 200;
    setTimeout(() => {
        if(idRulare !== idRulareAnimatie) return;
        trimiteDrumLaHarta(drumComplet).catch((eroare) => {
            console.error(eroare);
            alert("Drumul a fost calculat, dar proiectarea pe harta a esuat.");
        });
    }, intarziereProiectie);
}

function calculatePath(){
    ruleazaNavigatia();
}