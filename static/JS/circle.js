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

    // 생성자
    constructor (x, y, radius, dx, dy, r, g, b, info) {
        super(); // Vector 상속
        this.x = x;
        this.y = y;
        this.radius = radius;

        // (dx == 0 OR dy == 0)인 경우가 없도록 함
        this.dx = dx || 1;
        this.dy = dy || -1;
        
        this.red = r;
        this.green = g;
        this.blue = b;
        
        this.info = info; // 'H:M count', count: 해당 시간의 인체 감지 횟수 
    }   

    draw() {
        /* 원 그리기 */

        context.beginPath();
        context.arc(this.x, this.y, this.radius, 0, PI);
        context.fillStyle = 
            `rgba(${this.red}, ${this.green}, ${this.blue}, 0.35)`; // 투명도: 0.35
        context.fill();
    }
    
    acc() {
        /* 원 움직이기 */

        const posX = this.x + this.dx; // 현재의 x좌표에 dx만큼 더함
        const posY = this.y + this.dy; // 현재의 y좌표에 dy만큼 더함
    
        // 원의 경계가 프레임(canvas)을 벗어나느 값이면 이동 방향 바꿈
        if (posX > canvas.width - this.radius || posX < this.radius)
          this.dx = -this.dx;
    
        if (posY > canvas.height - this.radius || posY < this.radius)
          this.dy = -this.dy;

        this.x += this.dx; // x좌표 위치 갱신
        this.y += this.dy; // y좌표 위치 갱신
    
        this.draw(); // 변경된 내용으로 원 다시 그리기
    }

    text() {
        /* 원의 중심에 텍스트, 그리기 */

        // 글자가 원의 중심에 위치하도록 함
        context.textBaseline = "middle";
        context.textAlign = "center";

        context.strokeStyle = "#242424";
        context.font = "normal 20px Roboto";
        context.lineWidth = 1;
        
        context.strokeText(this.info, this.x, this.y); // 원 위의 시간, 감지 횟수 정보 텍스트를 그림
    }
}

function play() {
    /* 애니메이션 시작 */
    context.clearRect(0, 0, canvas.width, canvas.height);
    layer();
    raf = window.requestAnimationFrame(play);
}

function pause() {
    /* 애니메이션 중지 */
    window.cancelAnimationFrame(raf);
}
