// get images from server
const server = document.getElementById("openseadragon").dataset;
const sources = JSON.parse(server.urls);
let currentFn, currentDim;
let annotations = [];

// turn raw img list to usable tilesource obj list
let parsedSources = [];
for (let i = 0; i < sources.length; i++) {
    let res = {};
    res.type = "image";
    res.url = sources[i];
    parsedSources.push(res);
}

// init openseadragon img viewer
const viewer = OpenSeadragon({
    id: "openseadragon",
    prefixUrl: "/static/openseadragon/images/",
    tileSources: parsedSources,
    sequenceMode: true,
    showNavigator: true,
    navigatorPosition: "BOTTOM_RIGHT",
    animationTime: 0.5,
    showFullPageControl: false,
    maxZoomLevel: 5,
});

// init annotorious module
const anno = OpenSeadragon.Annotorious(viewer, {
    widgets: [],
    allowEmpty: true,
});
anno.setDrawingTool("polygon");

// store/update/delete annotations in separate array
// save to server every time a change is issued
anno.on("createAnnotation", (annotation) => {
    annotations.push(annotation);
    clientSaveAnnotation(currentFn, annotations);
});
anno.on("deleteAnnotation", (annotation) => {
    annotations = annotations.filter((a) => a.id !== annotation.id);
    clientSaveAnnotation(currentFn, annotations);
});
anno.on("updateAnnotation", (annotation) => {
    annotations = annotations.filter((a) => a.id !== annotation.id);
    annotations.push(annotation);
    clientSaveAnnotation(currentFn, annotations);
});

// openseadragon viewer handlers
viewer.addHandler("open", (e) => {
    console.log(e);
    // open + track annotations
    const splt = e.source.url.split("/");
    currentFn = splt[splt.length - 1];
    currentDim = { dimensions: e.eventSource.source.dimensions };
    fetch(`/files/getAnnotation/${currentFn.split(".")[0] + ".json"}`)
        .then((res) => {
            res.json().then((data) => {
                // remove dimensions from annotation data
                data.shift();
                // display pre-existing annotations and append to tracking arr
                data.forEach((el) => annotations.push(el));
                anno.setAnnotations(data);
            });
        })
        .catch((err) => {
            alert(err);
        });
});
viewer.addHandler("page", (e) => {
    // save once more in case of empty annotation/previous failed saves
    clientSaveAnnotation(currentFn, annotations);
    // clear tracked annotations on new page
    anno.clearAnnotations();
    annotations = [];
});

// onclick listener for annotation discard button
document.getElementById("discardConfirm").onclick = () => {
    annotations = [];
    anno.clearAnnotations();
    clientSaveAnnotation(currentFn, annotations);
};

function clientSaveAnnotation(currentFn, annotations) {
    // send annotation to server for processing
    // include dimensions of the image as 0th elem
    if (annotations.length === 0) {
        annotations.unshift(currentDim);
    } else if (!("dimensions" in annotations[0])) {
        annotations.unshift(currentDim);
    }
    fetch(`/annotator/saveAnnotation/${currentFn}`, {
        method: "POST",
        body: JSON.stringify(annotations),
        headers: {
            "Content-Type": "application/json",
        },
    }).catch((err) => {
        alert(err);
    });
}
