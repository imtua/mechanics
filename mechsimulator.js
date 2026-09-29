const canvas = document.createElement("canvas");
canvas.id = "canvas";
const ctx = canvas.getContext("2d");
ctx.lineCap = "round";
const trailPoints = new Map();
const trailDuration = 1000;

const energyLabel = document.createElement("div");
energyLabel.id = "energy-label";
const metricsLabel = document.createElement("div");
metricsLabel.id = "metrics-label";
const conservedLabel = document.createElement("div");
conservedLabel.id = "conserved-label";
const parameterSummary = document.createElement("div");
parameterSummary.id = "parameter-summary";
const symbolContainer = document.createElement("div");
symbolContainer.id = "symbol-container";
symbolContainer.classList.add("fade-in");
const equationLabel = document.createElement("div");
equationLabel.id = "equation-label";
equationLabel.classList.add("fade-in");
const simulationLabel = document.createElement("div");
simulationLabel.id = "simulation-label";

const attributionLabel = document.createElement("div");
attributionLabel.id = "attribution-label";
attributionLabel.innerHTML = `Open sourced, made by <a href="https://github.com/imtua"><b>Imtiaz Ahamed</b></a>`;

const mechmathLink = document.createElement("a");
mechmathLink.id = "mechmath-link";
mechmathLink.href = "https://mechanics.help/mechmaths";
mechmathLink.textContent = "Learn how mechmath works";

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

const descriptionModal = document.createElement("div");
descriptionModal.id = "description-modal";
descriptionModal.innerHTML = `
<div id="description-modal-content" class="fade-in">
    <span>Description:</span>
    <div id="description-file"></div>
</div>
`;

const descriptionToggle = document.createElement("button");
descriptionToggle.id = "description-toggle";
descriptionToggle.innerHTML = "Description";

const homeLink = document.createElement("a");
homeLink.id = "home-link";
homeLink.href = "../";
homeLink.textContent = "Home";

const parametersToggle = document.createElement("button");
parametersToggle.id = "parameters-toggle";
parametersToggle.innerHTML = "Parameters";

const parametersPanel = document.createElement("div");
parametersPanel.id = "parameters-panel";
parametersPanel.innerHTML = "<strong>Simulation parameters</strong>";

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
<img src="../icons/reset.svg" class="playback-button">
<img src="../icons/pause.svg" class="playback-button">
<img src="../icons/step.svg" class="playback-button">
`;

document.body.prepend(
    canvas,
    energyLabel,
    metricsLabel,
    conservedLabel,
    parameterSummary,
    symbolContainer,
    equationLabel,
    simulationLabel,
    attributionLabel,
    mechmathLink,
    systemModal,
    modalToggle,
    descriptionModal,
    descriptionToggle,
    homeLink,
    parametersToggle,
    parametersPanel,
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

const descriptionFile = document.getElementById("description-file");
fetch("description.md")
    .then((r) => r.text())
    .then((text) => { descriptionFile.textContent = text; });

const descriptionModalContent = document.getElementById("description-modal-content");
const descriptionModalHandler = () => {
    descriptionModal.classList.toggle("shown");
    descriptionModalContent.classList.toggle("shown");
}
descriptionModal.addEventListener("click", () => {
    if (!descriptionModalContent.matches(":hover")) {
        descriptionModalHandler();
    }
});
descriptionToggle.addEventListener("click", descriptionModalHandler);
parametersToggle.addEventListener("click", () => {
    parametersPanel.classList.toggle("shown");
});

const systemScript = document.createElement("script");
systemScript.type = "mpy";
systemScript.src = "system.py?v=5";
systemScript.setAttribute("config", "../mechsimulator-conf.json?v=5");
document.body.append(systemScript);

MathJax = {
    svg: { blacker: 5 }
};

let mechasimulator = {
    title: "",
    symbols: {
        names: [],
        latex: []
    },
    metricLabels: [],
    metricVelocityLabels: [],
    metricUnits: [],
    metricVelocityUnits: []
}

window.addEventListener("load", () => {
    document.title = "Mechanics: " + mechasimulator.title;
    simulationLabel.innerHTML = mechasimulator.title;
});

MathJax.startup = {
    ready() {
        MathJax.startup.defaultReady();
        MathJax.startup.promise.then(() => {
            for (const symbol of mechasimulator.symbols.latex) {
                symbolContainer.textContent += "\\(" + symbol + "\\) ";
            }
            MathJax.typesetPromise([symbolContainer]).then(() => {
                const svgs = symbolContainer.querySelectorAll("svg");
                for (let i = 0; i < svgs.length; i++) {
                    let container = svgs[i].parentElement;
                    mechasimulator.symbols[mechasimulator.symbols.names[i]] = svgs[i];
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

function setParameterControls(parameters, values) {
    if (typeof parameters === "string") {
        parameters = JSON.parse(parameters);
    }
    if (typeof values === "string") {
        values = JSON.parse(values);
    }
    for (const parameter of parameters) {
        const row = document.createElement("label");
        row.className = "parameter-row";
        row.innerHTML = `
            <span>${parameter.label}</span>
            <input type="range" min="${parameter.min}" max="${parameter.max}"
                step="${parameter.step}" value="${values[parameter.name]}">
            <input type="number" min="${parameter.min}" max="${parameter.max}"
                step="${parameter.step}" value="${values[parameter.name]}">
        `;
        const range = row.children[1];
        const number = row.children[2];
        const update = (event) => {
            const value = Math.min(parameter.max, Math.max(parameter.min, Number(event.target.value)));
            range.value = value;
            number.value = value;
            if (window.applySimulationParameters != null) {
                window.applySimulationParameters(
                    parameters.map((item) => item.name === parameter.name ? value :
                        Number(document.querySelector(`[data-parameter="${item.name}"]`)?.value ??
                            values[item.name]))
                );
            }
        };
        range.dataset.parameter = parameter.name;
        number.dataset.parameter = parameter.name;
        range.addEventListener("input", update);
        number.addEventListener("change", update);
        parametersPanel.append(row);
    }
    parametersPanel.classList.add("available");
}

function setEnergyLabel(kinetic, potential) {
    const t = kinetic.toFixed(2);
    const v = potential.toFixed(2);
    const tv = (kinetic + potential).toFixed(2);
    energyLabel.textContent = `Kinetic: ${t} | Potential: ${v} | Total: ${tv}`;
    const energyMagnitude = Math.abs(kinetic) + Math.abs(potential);
    const kineticPercent = energyMagnitude === 0
        ? 0
        : Math.min(100, Math.max(0, Math.abs(kinetic) / energyMagnitude * 100));
    kineticBar.style.height = kineticPercent + "%";
}

function setMetrics(time, angles, velocities) {
    const angleNames = mechasimulator.symbols.names.filter((name) => name.startsWith("t"));
    metricsLabel.innerHTML = `<div>Time: ${time.toFixed(2)} s</div>`;
    for (let i = 0; i < angles.length; i++) {
        const suffix = angleNames[i]?.slice(1) || "";
        const label = mechasimulator.metricLabels[i] ||
            (suffix ? `θ${suffix}` : "θ");
        const unit = mechasimulator.metricUnits[i] || "rad";
        metricsLabel.innerHTML += `<div>${label}: ${angles[i].toFixed(2)} ${unit}</div>`;
        const velocityLabel = mechasimulator.metricVelocityLabels[i] ||
            (suffix ? `ω${suffix}` : "ω");
        const velocityUnit = mechasimulator.metricVelocityUnits[i] || `${unit}/s`;
        metricsLabel.innerHTML += `<div>${velocityLabel}: ${velocities[i].toFixed(2)} ${velocityUnit}</div>`;
    }

}

function setConservedLabel(velocities, constants, params) {
    if (typeof mechasimulator.conservedQuantity !== "function") {
        conservedLabel.textContent = "";
        return;
    }
    const quantities = mechasimulator.conservedQuantity(
        velocities, constants, params
    );
    const entries = Array.isArray(quantities[0]) ? quantities : [quantities];
    conservedLabel.innerHTML = entries
        .map(([value, label]) => `${label}: ${value.toFixed(3)}`)
        .join("<br>");
}

function setParameterSummary(constants) {
    if (typeof mechasimulator.parameterSummary !== "function") {
        parameterSummary.textContent = "";
        return;
    }
    parameterSummary.textContent = mechasimulator.parameterSummary(constants);
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

function drawTrailPoint(color = "blue") {
    const now = performance.now();
    const point = getWorld(0, 0);
    const points = trailPoints.get(color) || [];
    trailPoints.set(color, points);
    points.push({ x: point.x, y: point.y, time: now });

    while (points.length > 1 && now - points[0].time > trailDuration) {
        points.shift();
    }

    const transform = ctx.getTransform();
    const strokeStyle = ctx.strokeStyle;
    const lineWidth = ctx.lineWidth;
    const lineDash = ctx.getLineDash();
    ctx.resetTransform();
    ctx.lineWidth = 2.5;
    ctx.setLineDash([]);
    const trailColors = {
        blue: [50, 85, 255],
        green: [45, 180, 85],
        red: [220, 65, 65]
    };
    const trailColor = trailColors[color] || trailColors.blue;
    for (let i = 1; i < points.length; i++) {
        const age = now - points[i].time;
        const opacity = Math.max(0, 1 - age / trailDuration);
        if (opacity === 0) {
            continue;
        }
        ctx.strokeStyle = `rgba(${trailColor[0]}, ${trailColor[1]}, ${trailColor[2]}, ${opacity})`;
        ctx.beginPath();
        ctx.moveTo(points[i - 1].x, points[i - 1].y);
        ctx.lineTo(points[i].x, points[i].y);
        ctx.stroke();
    }
    ctx.setTransform(transform);
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = lineWidth;
    ctx.setLineDash(lineDash);
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
    angle %= 2 * Math.PI;
    if (angle < -Math.PI) {
        angle += 2 * Math.PI;
    } else if (angle > Math.PI) {
        angle -= 2 * Math.PI;
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
    if (mechasimulator.symbols[name] != null) {
        let canvasPoint = getWorld(x, y);
        let x2 = "calc(" + canvasPoint.x + "px - 50%)";
        let y2 = "calc(" + canvasPoint.y + "px - 50%)";
        mechasimulator.symbols[name].style.transform = "translate(" + x2 + "," + y2 + ")";
        mechasimulator.symbols[name].style.visibility = "visible";
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
    trailPoints.clear();
}

window.addEventListener("load", resize);
window.addEventListener("resize", resize);