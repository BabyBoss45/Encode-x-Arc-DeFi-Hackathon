// Custom Date Picker - SuperOffice Style
class DatePicker {
    constructor(inputElement, options = {}) {
        this.input = inputElement;
        this.options = {
            format: options.format || 'YYYY-MM-DD',
            minDate: options.minDate || null,
            maxDate: options.maxDate || null,
            ...options
        };
        
        this.currentDate = new Date();
        this.selectedDate = null;
        this.viewMode = 'days'; // 'days', 'months', 'years'
        
        this.init();
    }
    
    init() {
        // Create wrapper
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'datepicker-wrapper';
        this.input.parentNode.insertBefore(this.wrapper, this.input);
        this.wrapper.appendChild(this.input);
        
        // Create calendar
        this.calendar = document.createElement('div');
        this.calendar.className = 'datepicker-calendar';
        this.wrapper.appendChild(this.calendar);
        
        // Set initial value
        if (this.input.value) {
            this.selectedDate = this.parseDate(this.input.value);
            this.currentDate = new Date(this.selectedDate);
        }
        
        // Event listeners
        this.input.addEventListener('click', () => this.toggle());
        this.input.addEventListener('focus', () => this.show());
        this.input.readOnly = true;
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.wrapper.contains(e.target)) {
                this.hide();
            }
        });
        
        this.render();
    }
    
    parseDate(dateString) {
        if (!dateString) return new Date();
        const parts = dateString.split('-');
        if (parts.length === 3) {
            return new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
        }
        return new Date(dateString);
    }
    
    formatDate(date) {
        if (!date) return '';
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
    
    toggle() {
        if (this.calendar.classList.contains('active')) {
            this.hide();
        } else {
            this.show();
        }
    }
    
    show() {
        this.calendar.classList.add('active');
        this.render();
    }
    
    hide() {
        this.calendar.classList.remove('active');
    }
    
    render() {
        if (this.viewMode === 'days') {
            this.renderDays();
        } else if (this.viewMode === 'months') {
            this.renderMonths();
        } else if (this.viewMode === 'years') {
            this.renderYears();
        }
    }
    
    renderDays() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const startDate = new Date(firstDay);
        startDate.setDate(startDate.getDate() - startDate.getDay());
        
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'];
        const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        
        this.calendar.innerHTML = `
            <div class="datepicker-header">
                <button class="datepicker-nav-btn" data-action="prev-month">‹</button>
                <div class="datepicker-month-year" style="cursor: pointer;" data-action="show-months">
                    ${monthNames[month]} ${year}
                </div>
                <button class="datepicker-nav-btn" data-action="next-month">›</button>
            </div>
            <div class="datepicker-weekdays">
                ${weekdays.map(day => `<div class="datepicker-weekday">${day}</div>`).join('')}
            </div>
            <div class="datepicker-days">
                ${this.generateDaysGrid(startDate, lastDay, month, today)}
            </div>
            <div class="datepicker-footer">
                <button class="datepicker-btn" data-action="today">Today</button>
                <button class="datepicker-btn primary" data-action="clear">Clear</button>
            </div>
        `;
        
        this.attachEventListeners();
    }
    
    generateDaysGrid(startDate, lastDay, currentMonth, today) {
        let html = '';
        const currentDate = new Date(startDate);
        const selectedDateStr = this.selectedDate ? this.formatDate(this.selectedDate) : null;
        const todayStr = this.formatDate(today);
        
        for (let i = 0; i < 42; i++) {
            const dateStr = this.formatDate(currentDate);
            const isOtherMonth = currentDate.getMonth() !== currentMonth;
            const isToday = dateStr === todayStr;
            const isSelected = dateStr === selectedDateStr;
            const isDisabled = this.isDateDisabled(currentDate);
            
            let classes = 'datepicker-day';
            if (isOtherMonth) classes += ' other-month';
            if (isToday) classes += ' today';
            if (isSelected) classes += ' selected';
            
            html += `<button class="${classes}" 
                           data-date="${dateStr}" 
                           ${isDisabled ? 'disabled' : ''}
                           ${isDisabled ? '' : `data-action="select-day"`}>
                      ${currentDate.getDate()}
                    </button>`;
            
            currentDate.setDate(currentDate.getDate() + 1);
        }
        
        return html;
    }
    
    renderMonths() {
        const year = this.currentDate.getFullYear();
        const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        
        this.calendar.innerHTML = `
            <div class="datepicker-header">
                <button class="datepicker-nav-btn" data-action="prev-year">‹</button>
                <div class="datepicker-month-year" data-action="show-years">${year}</div>
                <button class="datepicker-nav-btn" data-action="next-year">›</button>
            </div>
            <div class="datepicker-month-selector">
                ${monthNames.map((month, index) => {
                    const isSelected = this.currentDate.getMonth() === index;
                    return `<div class="datepicker-month-item ${isSelected ? 'selected' : ''}" 
                                data-month="${index}" data-action="select-month">
                                ${month}
                            </div>`;
                }).join('')}
            </div>
        `;
        
        this.attachEventListeners();
    }
    
    renderYears() {
        const year = this.currentDate.getFullYear();
        const startYear = Math.floor(year / 10) * 10;
        const years = [];
        
        for (let i = startYear - 1; i <= startYear + 10; i++) {
            years.push(i);
        }
        
        this.calendar.innerHTML = `
            <div class="datepicker-header">
                <button class="datepicker-nav-btn" data-action="prev-decade">‹</button>
                <div class="datepicker-month-year">${startYear} - ${startYear + 9}</div>
                <button class="datepicker-nav-btn" data-action="next-decade">›</button>
            </div>
            <div class="datepicker-year-selector">
                ${years.map(y => {
                    const isSelected = this.currentDate.getFullYear() === y;
                    return `<div class="datepicker-year-item ${isSelected ? 'selected' : ''}" 
                                data-year="${y}" data-action="select-year">
                                ${y}
                            </div>`;
                }).join('')}
            </div>
        `;
        
        this.attachEventListeners();
    }
    
    attachEventListeners() {
        const actions = {
            'prev-month': () => {
                this.currentDate.setMonth(this.currentDate.getMonth() - 1);
                this.render();
            },
            'next-month': () => {
                this.currentDate.setMonth(this.currentDate.getMonth() + 1);
                this.render();
            },
            'prev-year': () => {
                this.currentDate.setFullYear(this.currentDate.getFullYear() - 1);
                this.render();
            },
            'next-year': () => {
                this.currentDate.setFullYear(this.currentDate.getFullYear() + 1);
                this.render();
            },
            'prev-decade': () => {
                this.currentDate.setFullYear(this.currentDate.getFullYear() - 10);
                this.render();
            },
            'next-decade': () => {
                this.currentDate.setFullYear(this.currentDate.getFullYear() + 10);
                this.render();
            },
            'select-day': (e) => {
                const dateStr = e.target.getAttribute('data-date');
                this.selectDate(this.parseDate(dateStr));
            },
            'select-month': (e) => {
                const month = parseInt(e.target.getAttribute('data-month'));
                this.currentDate.setMonth(month);
                this.viewMode = 'days';
                this.render();
            },
            'select-year': (e) => {
                const year = parseInt(e.target.getAttribute('data-year'));
                this.currentDate.setFullYear(year);
                this.viewMode = 'months';
                this.render();
            },
            'show-months': () => {
                this.viewMode = 'months';
                this.render();
            },
            'show-years': () => {
                this.viewMode = 'years';
                this.render();
            },
            'today': () => {
                this.selectDate(new Date());
            },
            'clear': () => {
                this.selectedDate = null;
                this.input.value = '';
                this.hide();
                this.input.dispatchEvent(new Event('change'));
            }
        };
        
        this.calendar.addEventListener('click', (e) => {
            const action = e.target.getAttribute('data-action');
            if (action && actions[action]) {
                e.preventDefault();
                e.stopPropagation();
                actions[action](e);
            }
        });
    }
    
    selectDate(date) {
        if (this.isDateDisabled(date)) return;
        
        this.selectedDate = date;
        this.input.value = this.formatDate(date);
        this.hide();
        this.input.dispatchEvent(new Event('change', { bubbles: true }));
    }
    
    isDateDisabled(date) {
        if (this.options.minDate) {
            const minDate = this.parseDate(this.options.minDate);
            if (date < minDate) return true;
        }
        if (this.options.maxDate) {
            const maxDate = this.parseDate(this.options.maxDate);
            if (date > maxDate) return true;
        }
        return false;
    }
}

// Initialize date pickers on page load
document.addEventListener('DOMContentLoaded', function() {
    // Auto-initialize all inputs with class 'datepicker' or type='date'
    document.querySelectorAll('input[type="date"], input.datepicker').forEach(input => {
        new DatePicker(input);
    });
});

// Export for manual initialization
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DatePicker;
}

