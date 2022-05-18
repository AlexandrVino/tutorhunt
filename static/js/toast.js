class Toast {
    constructor(t) {
        this._title = !1 !== t.title && (t.title || "Title"), this._text = t.text || "Message...", this._theme = t.theme || "default", this._autohide = t.autohide && !0, this._interval = +t.interval || 5e3, this._create(), this._el.addEventListener("click", t => {
            t.target.classList.contains("toast__close") && this._hide()
        }), this._show()
    }

    _show() {
        this._el.classList.add("toast_showing"), this._el.classList.add("toast_show"), window.setTimeout(() => {
            this._el.classList.remove("toast_showing")
        }), this._autohide && setTimeout(() => {
            this._hide()
        }, this._interval)
    }

    _hide() {
        this._el.classList.add("toast_showing"), this._el.addEventListener("transitionend", () => {
            this._el.classList.remove("toast_showing"), this._el.classList.remove("toast_show"), this._el.remove()
        }, {once: !0});
        const t = new CustomEvent("hide.toast", {detail: {target: this._el}});
        document.dispatchEvent(t)
    }

    _create() {
        const t = document.createElement("div");
        t.classList.add("toast"), t.classList.add(`toast_${this._theme}`);
        let e = '{header}<div class="toast__body"></div><button class="toast__close" type="button"></button>';
        const s = !1 === this._title ? "" : '<div class="toast__header"></div>';
        if (e = e.replace("{header}", s), t.innerHTML = e, this._title ? t.querySelector(".toast__header").textContent = this._title : t.classList.add("toast_message"), t.querySelector(".toast__body").textContent = this._text, this._el = t, !document.querySelector(".toast-container")) {
            const t = document.createElement("div");
            t.classList.add("toast-container"), document.body.append(t)
        }
        document.querySelector(".toast-container").append(this._el)
    }
}