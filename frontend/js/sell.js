// Sell Analysis Page JavaScript

const { formatCurrency, formatNumber, showToast, fetchAPI } = window.AppUtils;

const form = document.getElementById('analyzeForm');
const loading = document.getElementById('loading');
const sellForm = document.getElementById('sellForm');
const results = document.getElementById('results');
const resultsContent = document.getElementById('resultsContent');

// Form submission
if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const commodity = document.getElementById('commodity').value;
        const quantity = parseFloat(document.getElementById('quantity').value);
        const cost = parseFloat(document.getElementById('cost').value);
        const state = document.getElementById('state').value;
        
        // Show loading
        sellForm.classList.add('hidden');
        loading.classList.remove('hidden');
        results.classList.add('hidden');
        
        try {
            // Get user location
            const location = await window.AppUtils.getUserLocation();
            
            const requestData = {
                commodity,
                quantity,
                costPerQuintal: cost,
                userLocation: {
                    state,
                    lat: location.lat,
                    lng: location.lng
                }
            };
            
            const response = await fetch('https://agri-price-backend-p4yw.onrender.com/api/sell/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            loading.classList.add('hidden');
            
            if (data.success) {
                displayResults(data);
                results.classList.remove('hidden');
                showToast('Analysis complete!', 'success');
            } else {
                showToast(data.error || 'Analysis failed', 'error');
                sellForm.classList.remove('hidden');
            }
            
        } catch (error) {
            console.error('Error:', error);
            loading.classList.add('hidden');
            sellForm.classList.remove('hidden');
            showToast('An error occurred. Please try again.', 'error');
        }
    });
}

function displayResults(data) {
    const { decision, confidence, reasoning, bestMarket, alternativeMarkets, waitOption } = data;
    
    let html = '';
    
    // Decision badge
    let decisionClass = 'decision-neutral';
    let decisionEmoji = '📊';
    if (decision === 'SELL_NOW') {
        decisionClass = 'decision-sell';
        decisionEmoji = '✅';
    } else if (decision === 'WAIT') {
        decisionClass = 'decision-wait';
        decisionEmoji = '⏳';
    }
    
    html += `
        <div class="text-center mb-8 fade-in">
            <h2 class="text-4xl font-bold mb-4 text-gray-800">📊 Analysis Complete</h2>
            <span class="${decisionClass}">
                ${decisionEmoji} ${decision.replace('_', ' ')}
            </span>
            <p class="text-gray-600 mt-3 text-lg">Confidence: ${confidence}%</p>
            <div style="background: #E5E7EB; height: 8px; border-radius: 4px; margin-top: 1rem; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #10B981, #059669); height: 100%; width: ${confidence}%; transition: width 1s ease;"></div>
            </div>
        </div>
    `;
    
    // Reasoning
    html += `
        <div class="mb-6 fade-in">
            <h3 class="text-2xl font-bold mb-4 text-gray-800">💡 Why?</h3>
            <ul class="space-y-3">
    `;
    reasoning.forEach(reason => {
        html += `
            <li style="display: flex; align-items: start; padding: 0.75rem; background: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <span style="margin-right: 0.75rem; color: #10B981; font-size: 1.25rem;">•</span>
                <span style="color: #4B5563; font-size: 1.05rem;">${reason}</span>
            </li>
        `;
    });
    html += `</ul></div>`;
    
    // Best Market
    html += `
        <div class="recommendation-card mb-6 fade-in" style="animation-delay: 0.1s;">
            <h3 class="text-2xl font-bold mb-4 text-gray-800">🏆 Best Market</h3>
            <div class="grid grid-cols-2 gap-4">
                <div style="background: white; padding: 1rem; border-radius: 0.5rem;">
                    <p class="text-gray-600 text-sm mb-1">Market</p>
                    <p class="text-xl font-bold text-gray-800">📍 ${bestMarket.market_name}</p>
                    <p class="text-sm text-gray-500">${bestMarket.district}</p>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 0.5rem;">
                    <p class="text-gray-600 text-sm mb-1">Price</p>
                    <p class="text-xl font-bold text-gray-800">₹${bestMarket.price_per_quintal}/quintal</p>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 0.5rem;">
                    <p class="text-gray-600 text-sm mb-1">Distance</p>
                    <p class="text-xl font-bold text-gray-800">📏 ${bestMarket.distance} km</p>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 0.5rem;">
                    <p class="text-gray-600 text-sm mb-1">Profit Margin</p>
                    <p class="text-xl font-bold profit-positive">📈 ${bestMarket.profit_margin}%</p>
                </div>
            </div>
        </div>
    `;
    
    // Profit Breakdown
    html += `
        <div style="background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%); border-radius: 1rem; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);" class="fade-in">
            <h3 class="text-2xl font-bold mb-4 text-gray-800">💰 Profit Breakdown</h3>
            <div class="space-y-3">
                <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: white; border-radius: 0.5rem;">
                    <span style="color: #6B7280; font-weight: 500;">Selling Price:</span>
                    <span style="font-weight: 700; color: #1F2937;">₹${formatNumber(bestMarket.revenue)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: white; border-radius: 0.5rem;">
                    <span style="color: #6B7280; font-weight: 500;">Your Cost:</span>
                    <span style="font-weight: 700; color: #1F2937;">₹${formatNumber(bestMarket.cost)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: white; border-radius: 0.5rem;">
                    <span style="color: #6B7280; font-weight: 500;">Transport:</span>
                    <span style="font-weight: 700; color: #1F2937;">₹${formatNumber(bestMarket.transport_cost)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: white; border-radius: 0.5rem;">
                    <span style="color: #6B7280; font-weight: 500;">Commission (2%):</span>
                    <span style="font-weight: 700; color: #1F2937;">₹${formatNumber(bestMarket.commission)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: white; border-radius: 0.5rem;">
                    <span style="color: #6B7280; font-weight: 500;">Loading/Unloading:</span>
                    <span style="font-weight: 700; color: #1F2937;">₹${formatNumber(bestMarket.loading_cost)}</span>
                </div>
                <hr style="border-color: #E5E7EB; margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; padding: 1rem; background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border-radius: 0.5rem; border: 2px solid #10B981;">
                    <span style="font-weight: 700; font-size: 1.25rem; color: #1F2937;">Net Profit:</span>
                    <span class="profit-positive" style="font-size: 1.5rem;">₹${formatNumber(bestMarket.net_profit)}</span>
                </div>
            </div>
        </div>
    `;
    
    // Alternative Markets
    if (alternativeMarkets && alternativeMarkets.length > 0) {
        html += `
            <div class="mb-6 fade-in" style="animation-delay: 0.2s;">
                <h3 class="text-2xl font-bold mb-4 text-gray-800">📍 Other Market Options</h3>
                <div class="space-y-3">
        `;
        
        alternativeMarkets.forEach((market, index) => {
            const isProfitable = market.net_profit > 0;
            html += `
                <div class="market-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="font-weight: 700; font-size: 1.125rem; color: #1F2937;">
                                ${index + 2}. ${market.market_name}
                            </p>
                            <p style="color: #6B7280; font-size: 0.875rem; margin-top: 0.25rem;">
                                ${market.distance} km • ₹${market.price_per_quintal}/quintal
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <p style="font-weight: 700; font-size: 1.25rem;" class="${isProfitable ? 'profit-positive' : 'profit-negative'}">
                                ₹${formatNumber(market.net_profit)}
                            </p>
                            <p style="color: #6B7280; font-size: 0.875rem;">
                                ${market.profit_margin}% margin
                            </p>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += `</div></div>`;
    }
    
    // Wait Option
    if (waitOption) {
        const riskColor = waitOption.risk === 'high' ? '#EF4444' : waitOption.risk === 'medium' ? '#F59E0B' : '#10B981';
        
        html += `
            <div style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border-left: 4px solid #F59E0B; border-radius: 1rem; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px rgba(245, 158, 11, 0.1);" class="fade-in">
                <h3 class="text-2xl font-bold mb-4" style="color: #92400E;">⏳ Wait Option</h3>
                <div class="grid grid-cols-2 gap-4 mb-4">
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem;">
                        <p style="color: #6B7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Wait Days</p>
                        <p style="font-weight: 700; font-size: 1.25rem; color: #92400E;">${waitOption.days} days</p>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem;">
                        <p style="color: #6B7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Expected Price</p>
                        <p style="font-weight: 700; font-size: 1.25rem; color: #92400E;">₹${waitOption.expectedPrice}/quintal</p>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem;">
                        <p style="color: #6B7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Extra Profit Potential</p>
                        <p style="font-weight: 700; font-size: 1.25rem; color: #10B981;">+₹${formatNumber(waitOption.potentialExtraProfit)}</p>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem;">
                        <p style="color: #6B7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Risk Level</p>
                        <p style="font-weight: 700; font-size: 1.25rem; color: ${riskColor}; text-transform: uppercase;">${waitOption.risk}</p>
                    </div>
                </div>
                ${waitOption.riskFactors ? `
                    <div style="background: white; padding: 1rem; border-radius: 0.5rem;">
                        <p style="font-weight: 700; margin-bottom: 0.5rem; color: #92400E;">⚠️ Risk Factors:</p>
                        <ul style="font-size: 0.875rem; color: #6B7280;">
                            ${waitOption.riskFactors.map(risk => `<li style="margin-bottom: 0.25rem;">• ${risk}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    // Action Buttons
    html += `
        <div style="display: flex; gap: 1rem; margin-top: 2rem;" class="fade-in">
            <button onclick="location.reload()" class="btn-primary" style="flex: 1;">
                🔄 New Analysis
            </button>
            <button onclick="window.print()" class="btn-secondary" style="flex: 1;">
                🖨️ Print Report
            </button>
        </div>
    `;
    
    resultsContent.innerHTML = html;
}
