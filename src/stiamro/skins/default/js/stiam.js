var Newz = {version: '2.0'};

Newz.Events = {};
Newz.Events.CLICK = 'newz.events.click.in';
Newz.Events.CLOSE = 'newz.events.close';
Newz.Events.EXIT = 'newz.events.exit';

Newz.Popup = {
  initialize: function(){
    var self = this;
    this.area = jQuery('<div>').attr('id', 'image_overlay');

    this.leftside = jQuery('<div>').addClass('left');
    this.image = jQuery('<img>');
    this.leftside.append(this.image);

    this.rightside = jQuery('<div>').addClass('right').css('color', 'white');
    this.title = jQuery('<h3>');
    this.description = jQuery('<h4>');
    this.bottom = jQuery('<div>').addClass('underline');
    this.rightside.append(this.title).append(this.description);

    this.area.append(this.leftside).append(this.rightside).append(this.bottom);

    jQuery('body').append(this.area);

    // Events
    jQuery(Newz.Events).bind(Newz.Events.CLICK, function(evt, data){
      self.update(data.link);
    });
  },

  update: function(link){
    var self = this;
    jQuery.get(link, {}, function(data){
      data = jQuery(data);
      var title = jQuery('.n-link', data);
      self.title.text(title.text());

      var description = jQuery('.n-content', data);
      self.description.text(description.text());

      var image = jQuery('.n-image img', data);
      if(image.length){
        image = image.attr('src');
        image = image.replace('@@scale/album', '@@scale/large');
        self.image.attr('src', image);
        self.image.show();
        self.rightside.removeClass('right-full');
      }else{
        self.image.hide();
        self.rightside.addClass('right-full');
      }

      var url = jQuery('.n-url', data);
      url.removeClass('n-url').addClass('url');
      jQuery('a', url).click(function(){
        var exit = '/exit' + title.attr('ajax');
        jQuery(Newz.Events).trigger(Newz.Events.EXIT, {link: exit});
      });
      self.bottom.html(url);

      var bottom = jQuery('.n-share', data);
      bottom.removeClass('n-share').addClass('share');
      self.bottom.append(bottom);
    });
  }
};

Newz.Image = {
  initialize: function(){
    jQuery('.fancy-content').attr('rel', '#image_overlay');
    jQuery('.fancy-content').overlay({
      mask: 'black',
      onBeforeLoad: function() {
        var trigger = this.getTrigger();
        var parent = trigger.parent().parent();
        var link = jQuery('.n-link', parent);
        var href = link.attr('href');
        href += '/content.html';
        jQuery(Newz.Events).trigger(Newz.Events.CLICK, {
          link: href,
          hash: link.attr('ajax')
        });
      },
      onClose: function(){
        jQuery(Newz.Events).trigger(Newz.Events.CLOSE);
      }
    });
  }
};

Newz.Content = {
  initialize: function(){
    jQuery('a.n-link').attr('rel', '#image_overlay');
    jQuery('a.n-link').overlay({
      mask: 'black',
      onBeforeLoad: function() {
        var trigger = this.getTrigger();
        var link = trigger.attr('href');
        link += '/content.html';
        jQuery(Newz.Events).trigger(Newz.Events.CLICK, {
          link: link,
          hash: trigger.attr('ajax')
          });
      },
      onClose: function(){
        jQuery(Newz.Events).trigger(Newz.Events.CLOSE);
      }
    });
    jQuery('.newsitem .n-url a').click(function(){
      var exit = jQuery(this).parent().parent().parent();
      exit = '/exit' + jQuery('.n-link', exit).attr('ajax');
      jQuery(Newz.Events).trigger(Newz.Events.EXIT, {link: exit});
    });
  }
};

Newz.Sidebar = {
  initialize: function(){
    jQuery('.right-link a').attr('rel', '#image_overlay');
    jQuery('.right-link a').overlay({
      mask: 'black',
      onBeforeLoad: function() {
        var trigger = this.getTrigger();
        var link = trigger.attr('href');
        link += '/content.html';
        jQuery(Newz.Events).trigger(Newz.Events.CLICK, {
          link: link,
          hash: trigger.attr('ajax')
        });
      },
      onClose: function(){
        jQuery(Newz.Events).trigger(Newz.Events.CLOSE);
      }
    });

    jQuery('.right-image a').attr('rel', '#image_overlay');
    jQuery('.right-image a').overlay({
      mask: 'black',
      onBeforeLoad: function() {
        var trigger = this.getTrigger();
        var parent = trigger.parent().parent();
        var link = jQuery('.right-link a', parent);
        var href = link.attr('href');
        href += '/content.html';
        jQuery(Newz.Events).trigger(Newz.Events.CLICK, {
          link: href,
          hash: link.attr('ajax')
        });
      },
      onClose: function(){
        jQuery(Newz.Events).trigger(Newz.Events.CLOSE);
      }
    });
  }
};

Newz.Location = {
  initialize: function(){
    var self = this;
    // Events
    jQuery(Newz.Events).bind(Newz.Events.CLICK, function(evt, data){
      if(data.hash){
        self.set(data.hash);
      }
    });

    this.hash = this.get();
    if(!this.hash.match('/sursa/')){
      return;
    }

    // Init
    var a = jQuery('<a>').attr('rel', '#image_overlay');
    a.overlay({
      mask: 'black',
      onBeforeLoad: function() {
        var link = self.hash;
        jQuery(Newz.Events).trigger(Newz.Events.CLICK, {link: link});
      },
      onClose: function(){
        jQuery(Newz.Events).trigger(Newz.Events.CLOSE);
      }
    });
    a.click();
    var exit = '/ajax' + this.hash;
    jQuery(Newz.Events).trigger(Newz.Events.EXIT, {link: exit});
  },

  get: function(){
    var r = window.location.href;
    var i = r.indexOf("#");
    var hash = (i >= 0 ? r.substr(i+1) : '');
    return hash;
  },

  set: function(hash){
    this.hash = hash;
    if(!this.hash){
      document.location.hash = '#';
    }else{
      document.location.hash = '#' + this.hash;
      var exit = '/ajax' + this.hash;
      jQuery(Newz.Events).trigger(Newz.Events.EXIT, {link: exit});
    }
  }
};

Newz.Google = {
  initialize: function(){
    var self = this;
    this.tracker = window.pageTracker;
    // Events
    jQuery(Newz.Events).bind(Newz.Events.EXIT, function(evt, data){
      self.track(data.link);
    });
  },

  track: function(url){
    if(!this.tracker){
      return;
    }
    this.tracker._trackPageview(url);
  }
};

Newz.Date = {
  initialize: function(){
    var dates = jQuery('.n-byline');
    var context = this;
    dates.each(function(){
      var date = jQuery(this);
      context.format(date);
    });
  },

  format: function(date){
    var now = jQuery('#current-time').text();
    if(now){
      now = new Date(now);
    }else{
      now = new Date();
    }
    var past = new Date(date.text());
    var delta = (now-past)/1000;
    if(delta < 0){
      date.text('acum cateva secunde');
      return;
    }
    // Minutes
    if(delta < 120){
      date.text('acum un minut');
      return;
    }
    if(delta < 3300){
      var min = parseInt(delta/60, 10);
      date.text('acum ' + min + ' minute');
      return;
    }
    // Hours
    if(delta < 7200){
      date.text('acum o ora');
      return;
    }
    if(delta < 72000){
      var hours = parseInt(delta / 3600, 10);
      date.text('acum ' + hours + ' ore');
      return;
    }
    // Days
    delta = delta / 3600;
    if(delta < 48){
      date.text('ieri');
      return;
    }
    if(delta < 160){
      var days = parseInt(delta / 24, 10);
      date.text('acum ' + days + ' zile');
      return;
    }
    // Weeks
    if(delta < 336){
      date.text('saptamana trecuta');
      return;
    }
    if(delta < 720){
      var weeks = parseInt(delta/24/7, 10);
      date.text('acum ' + weeks + ' saptamani');
      return;
    }
    // Months
    delta = delta / 24;
    if(delta < 60){
      date.text('acum o luna');
      return;
    }
    if(delta < 360){
      var months = parseInt(delta/30, 10);
      date.text('acum ' + months + ' luni');
      return;
    }
    // Years
    if(delta < 720){
      date.text('acum un an');
      return;
    }
    if(delta>720){
      var years = parseInt(delta/360, 10);
      date.text('acum ' + years + ' ani');
    }
  }
};

Newz.Status = {
  initialize: function(){
    this.drawer = jQuery('<div>').attr('id', 'messages');
    jQuery('body').prepend(this.drawer);
    this.drawer.text('Revista presei romanesti');
    var self = this;
    this.drawer.click(function(){
      self.drawer.slideUp();
    });
  },

  message: function(msg){
    this.drawer.html(msg);
    this.drawer.slideDown();
  }
};

Newz.load = function(){

  Newz.Date.initialize();
  Newz.Status.initialize();

  // Disabled for handheld
  // XXX Find a better way to check handheld or not
  if(jQuery('#google_search:hidden').length){
    return;
  }

  Newz.Google.initialize();
  Newz.Popup.initialize();
  Newz.Content.initialize();
  Newz.Sidebar.initialize();
  Newz.Image.initialize();
  Newz.Location.initialize();

};

jQuery(document).ready(Newz.load);
