var canvas = document.querySelector("#myCanvas");

if(!canvas){
    throw new Error("canvas is undefined");
}

var context = canvas.getContext("2d");
var raf = null; // 애니메이션 컨트롤
var PI = Math.PI * 2; // 원주율

class Vector {
    x = 0;
    y = 0;
    dx = 0;
    dy = 0;
}

// 원 객체화
class Circle extends Vector {
    radius = 0;
    type = "circle";

    colorCode = "#ffffff";

    // 생성자
    constructor (x, y, radius, dx, dy, r, g, b) {
        super(); // 상속
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.dx = dx || 1;
        this.dy = dy || -1;
        this.red = r;
        this.green = g;
        this.blue = b;
    }   

    draw() {
        context.beginPath();
        context.arc(this.x, this.y, this.radius, 0, PI);
        context.fillStyle = 
            `rgba(${this.red}, ${this.green}, ${this.blue}, 0.35)`;
        // context.stroke();
        context.fill();
    }
    
    acc() {
        const posX = this.x + this.dx;
        const posY = this.y + this.dy;
    
        if (posX > canvas.width - this.radius || posX < this.radius) {
          this.dx = -this.dx;
        }
    
        if (posY > canvas.height - this.radius || posY < this.radius) {
          this.dy = -this.dy;
        }

        this.x += this.dx;
        this.y += this.dy;
    
        this.draw();
    }

    to(x, y) {
        this.x = x;
        this.y = y;
    
        this.draw();
    }

    text(comment) {
        const text = comment || `${this.x}, ${this.y}`;
        context.strokeStyle = "#242424";
        context.font = "normal 12px Roboto";
        context.lineWidth = 1;
        context.strokeText(text, this.x, this.y);
    }

    line(){
        context.strokeStyle = "#242424";
        context.lineWidth = 0.5;

        context.beginPath();
        context.moveTo(this.x, canvas.height);
        context.lineTo(this.x, 0);
        context.stroke();

        context.beginPath();
        context.moveTo(0, 0);
        context.lineTo(0, this.y);
        context.lineTo(canvas.width, this.y)
        context.stroke();
    }
}

function play() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    layer();
    raf = window.requestAnimationFrame(play);
}

function pause() {
    window.cancelAnimationFrame(raf);
}
