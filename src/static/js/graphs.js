window.onload = function () {
    const ctx = document.getElementById('myChart');
    data = {
        labels: dates,
        datasets: [{
            label: 'Price ($)',
            data: prices,
            fill: true,
            borderColor: 'rgb(223, 235, 227)',
            tension: 0.1
        }]
    }

    const chart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            title: {
                display: true,
                text: stock
            }
        }
    });

};

jQuery(document).ready(function ($) {
    $(function () {
        $('input[type=radio]').each(function () {
            var state = JSON.parse(localStorage.getItem('radio_' + this.id));

            if (state) this.checked = state.checked;
        });
    });

    $(window).bind('unload', function () {
        $('input[type=radio]').each(function () {
            localStorage.setItem(
                'radio_' + this.id, JSON.stringify({ checked: this.checked })
            );
        });
    });

    $('input[type=radio]').on('change', function () {
        $(this).closest("form").submit();
    });
    $('input[type=submit]').hide();
});
