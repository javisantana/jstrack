var Errors = Backbone.Model.extend({
    url: '/t/error',

    set_code: function(c) {
        this.url = '/' + c + this.url;
    }
});


var ERR_TMPL = '<li> \
                    <div class="times">{{times}}</div> \
                    <div class="error_content"> \
                        <p class="where">{{where}}</p> \
                        <p class="error">{{error}}</p> \
                        <p class="date"> Last time: {{date}}</p> \
                    </div> \
                </li>';

var ErrorView = Backbone.View.extend({
    el: $('.content'),
    err_template: ERR_TMPL,

    initialize: function() {
        _.bindAll(this, 'render');
        this.errors = this.options.errors;
        this.errors.bind('change',  this.render);
    },
    render: function(data) {
        var self = this;
        this.$('.total .big').html(this.errors.get('count'));
        this.$('.month .big').html(this.errors.get('count_month'));
        this.$('.today .big').html(this.errors.get('count_today'));
        var ul = this.$('.errors');
        ul.hide();
        ul.html('');
        _(this.errors.get('latest')).each(function(err) {
            ul.append(Mustache.to_html(self.err_template, { 
                    'where': function() {
                        return err.error.error.split('$')[0];
                    },
                    'times': err.times,
                    'error': function(){
                        return err.error.error.split('$$')[1];
                    },
                    'date': function() {
                        return prettyDate(parseInt(err.date, 10)*1000);
                    }
            }));
        });
        ul.fadeIn();
    }
});

var App = (function() {
    var errors = new Errors();
    var view = new ErrorView({errors: errors});

    function run(site_code) {
        errors.set_code(site_code);
        errors.fetch();
        setInterval(function() {
            //errors.fetch();
        }, 1000*30);
    }
    return {
        run: run
    }
})();
