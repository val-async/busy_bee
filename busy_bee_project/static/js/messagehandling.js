     // Wait for the page to load
 setTimeout(function() {
        let msg = document.getElementById("messages_container_inner");
        if (msg) {
            msg.style.transition = "opacity 1s";
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 1000); 
        }
    }, 2500);

    // auto dismiss after 3 secs
    function dismissMessage(id) {
        let element = document.getElementById(id);
        if (element) {
            element.style.opacity = '0';
            setTimeout(() => element.remove(), 3000); 
        }
    }


