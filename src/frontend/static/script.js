const grid = document.getElementById("grid");
let mode = "obstacle";
const rows = 5;
const cols = 5;
const cells = [];
const VISIT_DELAY_MS = 120;
let animationRunId = 0;

function trimiteDrumLaHarta(pathCells) {
    return fetch('/proiecteaza-harta', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: pathCells })
    }).then((response) => {
        if (!response.ok) {
            throw new Error('Serverul nu a putut proiecta drumul pe harta.');
        }
        window.location.href = '/map';
    });
}

function setMode(m){ mode = m; }

for(let i=0;i<rows;i++){
    cells[i]=[];
    for(let j=0;j<cols;j++){
        const cell = document.createElement("div");
        cell.classList.add("cell");

        cell.addEventListener("click", function(){
            if(mode==="obstacle"){
                cell.classList.remove("start","end","path","visited");
                cell.classList.add("obstacle");
            }else if(mode==="start"){
                document.querySelectorAll(".start").forEach(c=>c.classList.remove("start"));
                cell.classList.remove("obstacle","end","path","visited");
                cell.classList.add("start");
            }else if(mode==="end"){
                document.querySelectorAll(".end").forEach(c=>c.classList.remove("end"));
                cell.classList.remove("obstacle","start","path","visited");
                cell.classList.add("end");
            }
        });

        grid.appendChild(cell);
        cells[i][j]=cell;
    }
}

function calculatePath(){
    animationRunId += 1;
    const runId = animationRunId;

    document.querySelectorAll(".path").forEach(c=>c.classList.remove("path"));
    document.querySelectorAll(".visited").forEach(c=>c.classList.remove("visited"));
    const startCell = document.querySelector(".start");
    const endCell = document.querySelector(".end");
    if(!startCell || !endCell){ alert("Setează Start și Destination!"); return; }

    let startPos,endPos;
    for(let i=0;i<rows;i++)
        for(let j=0;j<cols;j++){
            if(cells[i][j]===startCell) startPos=[i,j];
            if(cells[i][j]===endCell) endPos=[i,j];
        }

    const openSet = [startPos];
    const prev = Array.from({length:rows},()=>Array(cols).fill(null));
    const gScore = Array.from({length:rows},()=>Array(cols).fill(Infinity));
    const fScore = Array.from({length:rows},()=>Array(cols).fill(Infinity));
    const directions=[[0,1],[1,0],[0,-1],[-1,0]];
    const visitedOrder = [];

    const heuristic = (x,y) => Math.abs(x - endPos[0]) + Math.abs(y - endPos[1]);

    gScore[startPos[0]][startPos[1]] = 0;
    fScore[startPos[0]][startPos[1]] = heuristic(startPos[0], startPos[1]);

    while(openSet.length){
        let bestIndex = 0;
        for(let i=1;i<openSet.length;i++){
            const [cx,cy] = openSet[i];
            const [bx,by] = openSet[bestIndex];
            if(fScore[cx][cy] < fScore[bx][by]) bestIndex = i;
        }

        const [x,y] = openSet.splice(bestIndex,1)[0];
        visitedOrder.push([x,y]);
        if(x===endPos[0] && y===endPos[1]) break;

        for(const [dx,dy] of directions){
            const nx=x+dx, ny=y+dy;
            if(nx<0 || nx>=rows || ny<0 || ny>=cols) continue;
            if(cells[nx][ny].classList.contains("obstacle")) continue;

            const tentativeG = gScore[x][y] + 1;
            if(tentativeG < gScore[nx][ny]){
                prev[nx][ny]=[x,y];
                gScore[nx][ny]=tentativeG;
                fScore[nx][ny]=tentativeG + heuristic(nx, ny);

                if(!openSet.some(([ox,oy]) => ox===nx && oy===ny)){
                    openSet.push([nx,ny]);
                }
            }
        }
    }

    if(startPos[0]!==endPos[0] || startPos[1]!==endPos[1]){
        if(prev[endPos[0]][endPos[1]]===null){
            visitedOrder.forEach(([vx, vy], index) => {
                setTimeout(() => {
                    if(runId !== animationRunId) return;
                    const cell = cells[vx][vy];
                    if(!cell.classList.contains("start") && !cell.classList.contains("end")){
                        cell.classList.add("visited");
                    }
                }, index * VISIT_DELAY_MS);
            });

            setTimeout(() => {
                if(runId !== animationRunId) return;
                alert("Nu există drum disponibil!");
            }, visitedOrder.length * VISIT_DELAY_MS);
            return;
        }
    }

    const pathCells = [];
    let pathPos=endPos;
    while(pathPos && (pathPos[0]!==startPos[0] || pathPos[1]!==startPos[1])){
        const [x,y]=pathPos;
        if(!cells[x][y].classList.contains("end")) pathCells.push([x,y]);
        pathPos=prev[x][y];
    }

    visitedOrder.forEach(([vx, vy], index) => {
        setTimeout(() => {
            if(runId !== animationRunId) return;
            const cell = cells[vx][vy];
            if(!cell.classList.contains("start") && !cell.classList.contains("end")){
                cell.classList.add("visited");
            }
        }, index * VISIT_DELAY_MS);
    });

    const pathStartDelay = visitedOrder.length * VISIT_DELAY_MS;
    pathCells.reverse().forEach(([px, py], index) => {
        setTimeout(() => {
            if(runId !== animationRunId) return;
            const cell = cells[px][py];
            cell.classList.remove("visited");
            cell.classList.add("path");
        }, pathStartDelay + index * VISIT_DELAY_MS);
    });

    const fullPath = (startPos[0] === endPos[0] && startPos[1] === endPos[1])
        ? [startPos]
        : [startPos, ...pathCells, endPos];

    const projectionDelay = pathStartDelay + (pathCells.length * VISIT_DELAY_MS) + 200;
    setTimeout(() => {
        if(runId !== animationRunId) return;
        trimiteDrumLaHarta(fullPath).catch((error) => {
            console.error(error);
            alert("Drumul a fost calculat, dar proiectarea pe harta a esuat.");
        });
    }, projectionDelay);
}