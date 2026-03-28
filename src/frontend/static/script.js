const grila = document.getElementById("grid");
let mod = "obstacle";
const randuri = 5;
const coloane = 5;
const celule = [];
const INTARZIERE_VIZITA_MS = 120;
let idRulareAnimatie = 0;

function trimiteDrumLaHarta(celuleDrum) {
    return fetch('/proiecteaza-harta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: celuleDrum })
    }).then((response) => {
        if (!response.ok) {
            throw new Error('Serverul nu a putut proiecta drumul pe harta.');
        }
        window.location.href = '/map';
    });
}

function setMode(modNou){ mod = modNou; }

for(let i=0;i<randuri;i++){
    celule[i]=[];
    for(let j=0;j<coloane;j++){
        const celula = document.createElement("div");
        celula.classList.add("cell");

        celula.addEventListener("click", function(){
            if(mod==="obstacle"){
                celula.classList.remove("start","end","path","visited");
                celula.classList.add("obstacle");
            }else if(mod==="start"){
                document.querySelectorAll(".start").forEach(c=>c.classList.remove("start"));
                celula.classList.remove("obstacle","end","path","visited");
                celula.classList.add("start");
            }else if(mod==="end"){
                document.querySelectorAll(".end").forEach(c=>c.classList.remove("end"));
                celula.classList.remove("obstacle","start","path","visited");
                celula.classList.add("end");
            }
        });

        grila.appendChild(celula);
        celule[i][j]=celula;
    }
}

function calculatePath(){
    idRulareAnimatie += 1;
    const idRulare = idRulareAnimatie;

    document.querySelectorAll(".path").forEach(c=>c.classList.remove("path"));
    document.querySelectorAll(".visited").forEach(c=>c.classList.remove("visited"));
    const celulaStart = document.querySelector(".start");
    const celulaFinal = document.querySelector(".end");
    if(!celulaStart || !celulaFinal){ alert("Setează Start și Destination!"); return; }

    let pozitieStart,pozitieFinal;
    for(let i=0;i<randuri;i++)
        for(let j=0;j<coloane;j++){
            if(celule[i][j]===celulaStart) pozitieStart=[i,j];
            if(celule[i][j]===celulaFinal) pozitieFinal=[i,j];
        }

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
            if(celule[nx][ny].classList.contains("obstacle")) continue;

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