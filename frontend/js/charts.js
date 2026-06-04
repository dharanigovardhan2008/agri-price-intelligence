// Charts.js - Price trend visualization

class PriceChart {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    }
    
    drawLineChart(data, options = {}) {
        if (!this.ctx) return;
        
        const {
            labels = [],
            values = [],
            color = '#10B981',
            title = 'Price Trend'
        } = options;
        
        const width = this.canvas.width;
        const height = this.canvas.height;
        const padding = 40;
        
        // Clear canvas
        this.ctx.clearRect(0, 0, width, height);
        
        // Draw title
        this.ctx.fillStyle = '#1F2937';
        this.ctx.font = 'bold 16px Inter';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(title, width / 2, 20);
        
        // Calculate scales
        const maxValue = Math.max(...values);
        const minValue = Math.min(...values);
        const valueRange = maxValue - minValue;
        
        const chartWidth = width - (padding * 2);
        const chartHeight = height - (padding * 2) - 20;
        
        const xStep = chartWidth / (values.length - 1);
        const yScale = chartHeight / valueRange;
        
        // Draw axes
        this.ctx.strokeStyle = '#E5E7EB';
        this.ctx.lineWidth = 1;
        
        // Y-axis
        this.ctx.beginPath();
        this.ctx.moveTo(padding, padding + 20);
        this.ctx.lineTo(padding, height - padding);
        this.ctx.stroke();
        
        // X-axis
        this.ctx.beginPath();
        this.ctx.moveTo(padding, height - padding);
        this.ctx.lineTo(width - padding, height - padding);
        this.ctx.stroke();
        
        // Draw line
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        
        values.forEach((value, index) => {
            const x = padding + (index * xStep);
            const y = height - padding - ((value - minValue) * yScale);
            
            if (index === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
        });
        
        this.ctx.stroke();
        
        // Draw points
        this.ctx.fillStyle = color;
        values.forEach((value, index) => {
            const x = padding + (index * xStep);
            const y = height - padding - ((value - minValue) * yScale);
            
            this.ctx.beginPath();
            this.ctx.arc(x, y, 4, 0, 2 * Math.PI);
            this.ctx.fill();
        });
        
        // Draw labels
        this.ctx.fillStyle = '#6B7280';
        this.ctx.font = '12px Inter';
        this.ctx.textAlign = 'center';
        
        labels.forEach((label, index) => {
            if (index % Math.ceil(labels.length / 6) === 0) {
                const x = padding + (index * xStep);
                this.ctx.fillText(label, x, height - padding + 20);
            }
        });
        
        // Draw value labels
        this.ctx.textAlign = 'right';
        const numYLabels = 5;
        for (let i = 0; i <= numYLabels; i++) {
            const value = minValue + (valueRange * i / numYLabels);
            const y = height - padding - (chartHeight * i / numYLabels);
            this.ctx.fillText('₹' + Math.round(value), padding - 10, y + 5);
        }
    }
}

// Export
window.PriceChart = PriceChart;