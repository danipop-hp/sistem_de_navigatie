const grid = document.getElementById("grid");
let mode = "obstacle";
const rows = 5;
const cols = 5;
const cells = [];

function setMode(m){ mode = m; }

for(let i=0;i<rows;i++){
    cells[i]=[];
    for(let j=0;j<cols;j++){
        const cell = document.createElement("div");
        cell.classList.add("cell");

        cell.addEventListener("click", function(){
            if(mode==="obstacle"){
                cell.classList.remove("start","end","path");
                cell.classList.add("obstacle");
            }else if(mode==="start"){
                document.querySelectorAll(".start").forEach(c=>c.classList.remove("start"));
                cell.classList.remove("obstacle","end","path");
                cell.classList.add("start");
            }else if(mode==="end"){
                document.querySelectorAll(".end").forEach(c=>c.classList.remove("end"));
                cell.classList.remove("obstacle","start","path");
                cell.classList.add("end");
            }
        });

        grid.appendChild(cell);
        cells[i][j]=cell;
    }
}

// BFS pentru calcul traseu
function calculatePath(){
    document.querySelectorAll(".path").forEach(c=>c.classList.remove("path"));
    const startCell = document.querySelector(".start");
    const endCell = document.querySelector(".end");
    if(!startCell || !endCell){ alert("Setează Start și Destination!"); return; }

    let startPos,endPos;
    for(let i=0;i<rows;i++)
        for(let j=0;j<cols;j++){
            if(cells[i][j]===startCell) startPos=[i,j];
            if(cells[i][j]===endCell) endPos=[i,j];
        }

    const queue = [startPos];
    const visited = Array.from({length:rows},()=>Array(cols).fill(false));
    const prev = Array.from({length:rows},()=>Array(cols).fill(null));
    visited[startPos[0]][startPos[1]]=true;
    const directions=[[0,1],[1,0],[0,-1],[-1,0]];

    while(queue.length){
        const [x,y]=queue.shift();
        if(x===endPos[0] && y===endPos[1]) break;
        for(const [dx,dy] of directions){
            const nx=x+dx, ny=y+dy;
            if(nx>=0 && nx<rows && ny>=0 && ny<cols &&
               !visited[nx][ny] && !cells[nx][ny].classList.contains("obstacle")){
                   queue.push([nx,ny]);
                   visited[nx][ny]=true;
                   prev[nx][ny]=[x,y];
            }
        }
    }

    let pathPos=endPos;
    while(pathPos && (pathPos[0]!==startPos[0] || pathPos[1]!==startPos[1])){
        const [x,y]=pathPos;
        if(!cells[x][y].classList.contains("end")) cells[x][y].classList.add("path");
        pathPos=prev[x][y];
    }
}