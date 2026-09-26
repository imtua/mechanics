const canvas = document.createElement("canvas");
canvas.id = "canvas";
const ctx = canvas.getContext("2d");
ctx.lineCap = "round";

const energyLabel = document.createElement("div");
energyLabel.id = "energy-label";
const symbolContainer = document.createElement("div");
symbolContainer.id = "symbol-container";
symbolContainer.classList.add("fade-in");
const equationLabel = document.createElement("div");
equationLabel.id = "equation-label";
equationLabel.classList.add("fade-in");
const simulationLabel = document.createElement("div");
simulationLabel.id = "simulation-label";

const systemModal = document.createElement("div");
systemModal.id = "system-modal";
systemModal.innerHTML = `
<div id="system-modal-content" class="fade-in">
    <span>Contents of <code>system.py</code>:</span>
    <div id="system-file"></div>
</div>
`;

const modalToggle = document.createElement("button");
modalToggle.id = "modal-toggle";
modalToggle.innerHTML = "Show/Hide system file.";

const energyBar = document.createElement("div");
energyBar.id = "energy-bar";
const kineticBar = document.createElement("div");
kineticBar.id = "kinetic-bar";
energyBar.append(kineticBar);
const energyBarLabel = document.createElement("div");
energyBarLabel.id = "energy-bar-label";
energyBarLabel.innerHTML = `
<div class="color-label" style="background-color: #EEE;"></div>
Kinetic&nbsp;
<div class="color-label" style="background-color: #AAA;"></div>
Potential
`;

const playbackContainer = document.createElement("div");
playbackContainer.id = "playback-container";
playbackContainer.innerHTML = `
<img src="icons/reset.svg" class="playback-button">
<img src="icons/pause.svg" class="playback-button">
<img src="icons/step.svg" class="playback-button">
`;

document.body.prepend(
    canvas,
    energyLabel,
    symbolContainer,
    equationLabel,
    simulationLabel,
    systemModal,
    modalToggle,
    energyBar,
    energyBarLabel,
    playbackContainer
);

const systemFile = document.getElementById("system-file");
fetch("system.py")
    .then((r) => r.text())
    .then((text) => { systemFile.innerHTML = text; });

const systemModalContent = document.getElementById("system-modal-content");
const modalHandler = () => {
    systemModal.classList.toggle("shown");
    systemModalContent.classList.toggle("shown");
}
systemModal.addEventListener("click", () => {
    if (!systemModalContent.matches(":hover")) {
        modalHandler();
    }
});
modalToggle.addEventListener("click", modalHandler);

const systemScript = document.createElement("script");
systemScript.type = "mpy";
systemScript.src = "system.py";
systemScript.setAttribute("config", "../mechsimulator-conf.json");
document.body.append(systemScript);

MathJax = {
    svg: { blacker: 5 }
};

let mechasim = {
    title: "",
    symbols: {
        names: [],
        latex: []
    }
}

window.addEventListener("load", () => {
    document.title = "Mechasim: " + mechasim.title;
    simulationLabel.innerHTML = mechasim.title;
});

MathJax.startup = {
    ready() {
        MathJax.startup.defaultReady();
        MathJax.startup.promise.then(() => {
            for (const symbol of mechasim.symbols.latex) {
                symbolContainer.textContent += "\\(" + symbol + "\\) ";
            }
            MathJax.typesetPromise([symbolContainer]).then(() => {
                const svgs = symbolContainer.querySelectorAll("svg");
                for (let i = 0; i < svgs.length; i++) {
                    let container = svgs[i].parentElement;
                    mechasim.symbols[mechasim.symbols.names[i]] = svgs[i];
                    symbolContainer.appendChild(svgs[i]);
                    container.remove();
                    svgs[i].style.removeProperty("vertical-align");
                }
                symbolContainer.classList.add("shown");
            })
        })
    }
}

function setEquationlabel(label) {
    equationLabel.textContent = label;
    MathJax.typesetPromise([equationLabel]).then(() => {
        equationLabel.classList.add("shown");
    });
}

function setEnergyLabel(kinetic, potential) {
    const t = kinetic.toFixed(2);
    const v = potential.toFixed(2);
    const tv = (kinetic + potential).toFixed(2);
    energyLabel.textContent = `Kinetic: ${t} | Potential: ${v} | Total: ${tv}`;
    kineticBar.style.height = (t / tv * 100) + "%";
}

function setPlaybackButtons(reset, toggle, step) {
    playbackContainer.children[0].addEventListener("click", () => {
        reset();
        playbackContainer.children[1].src = "../icons/play.svg";
    });
    playbackContainer.children[1].addEventListener("click", () => {
        if (toggle()) {
            playbackContainer.children[1].src = "../icons/play.svg";
        } else {
            playbackContainer.children[1].src = "../icons/pause.svg";
        }
    });
    playbackContainer.children[2].addEventListener("click", () => {
        step();
        playbackContainer.children[1].src = "../icons/play.svg";
    });
}

function resetCanvas() {
    ctx.resetTransform();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.translate(canvas.width / 3, canvas.height / 2);
}

function drawHinge() {
    drawCircle(4, "white", 2);
    drawCircle(0.5, "black", 0);
}

function drawBar(length, width = 3) {
    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, length);
    ctx.lineWidth = width;
    ctx.stroke();
}

function drawMass() {
    drawCircle(15, "black", 0);
}

function drawAxis(length) {
    ctx.setLineDash([2.5, 2.5]);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, length);
    ctx.lineWidth = 2;
    ctx.stroke();
}

function drawAngle(angle, radius) {
    angle = (angle = Math.PI) % (2 * Math.PI) - Math.PI;
    if (angle < -Math.PI) {
        angle += 2 * Math.PI;
    }
    ctx.setLineDash([2.5, 2.5]);
    ctx.beginPath();
    ctx.arc(0, 0, radius, angle + Math.PI / 2, Math.PI / 2, angle > 0);
    ctx.lineWidth = 2;
    ctx.stroke();
}

function drawSpring(spring, hinge = false) {
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(spring.start.x, spring.start.y);
    ctx.lineTo(spring.end.x, spring.end.y);
    ctx.lineWidth = 3;
    ctx.stroke();

    if (hinge) {
        ctx.translate(spring.start.x, spring.start.y);
        drawHinge();
        ctx.translate(-spring.start.x, -spring.start.y);

        ctx.translate(spring.end.x, spring.end.y);
        drawHinge();
        ctx.translate(-spring.end.x, -spring.end.y);
    }
}

function getWorld(x, y) {
    const point = new DOMPoint(x, y);
    const matrix = ctx.getTransform();
    return matrix.transformPoint(point);
}

function moveLabel(name, x, y) {
    if (mechasim.symbols[name] != null) {
        let canvasPoint = getWorld(x, y);
        let x2 = "calc(" + canvasPoint.x + "px - 50%";
        let y2 = "calc(" + canvasPoint.y + "px - 50% ";
        mechasim.symbols[name].style.transform = "translate(" + x2 + "," + y2 + ")";
    }
}

function drawPlane() {
    length = Math.max(canvas.width, canvas.height);
    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.moveTo(-length, 0);
    ctx.lineTo(length, 0);
    ctx.lineWidth = 3;
    ctx.stroke();
}

function drawCircle(radius, fill = "white", width = 3) {
    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, 2 * Math.PI);
    if (fill) {
        ctx.fillStyle = fill;
        ctx.fill();
    }
    ctx.lineWidth = width;
    ctx.stroke();
}

function drawSemi(radius, width = 3) {
    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI);
    ctx.lineWidth = width;
    ctx.stroke();
}

function drawDisk(radius, fill = "white", width = 3) {
    drawCircle(radius, fill, width)
    ctx.rotate(-Math.PI / 2);
    drawAxis(radius);
    ctx.rotate(Math.PI / 2);
}

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener("load", resize);
window.addEventListener("resize", resize);