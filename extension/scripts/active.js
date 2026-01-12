class Timer {
    constructor(options) {
        this.options = options;

        this.reset();
    }

    reset() {
        this.clock = 0;
        this.options.render(0);
    }

    update() {
        console.log("updating")
        const now = Date.now();
        const delta = now - this.offset;
        this.offset = now;

        this.clock += delta;

        console.log(this.clock);
        this.options.render(this.clock);
    }

    start() {
        this.offset = Date.now();
        setInterval(() => this.update(), this.options.delay);
    }
}

start.addEventListener("click", () => {
    // const timer = new Timer({delay: 1000, render: (time) => {
    //     timerText.value = Math.floor(time / 1000);
    // }})

    // timer.start();
})