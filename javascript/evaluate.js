 var button = document.getElementById("evalButton");
    var progress = document.getElementById("evalProgress");
    button.setAttribute("style", "display: none;");
    progress.value = 0;
    progress.setAttribute("style", ";");
    if (window.Worker) {
        var myWorker = new Worker("eval_webworker.js");
        myWorker.onmessage = function (e) {
            if (typeof e.data.percent != 'undefined') {
                progress.value = e.data.percent;
            }

            if (typeof e.data.mph != 'undefined') {
                progress.setAttribute("style", "display: none;");
                button.setAttribute("style", ";");
                swal({
                    title: "Evaluation complete",
                    text: "Average speed: <b>" + e.data.mph + " mph</b>",
                    html: true
                });
            }
        };
        myWorker.postMessage(getData());
    }