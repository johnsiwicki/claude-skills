<?php
global $siteTokens;
$fullpage = array (
    "index",
    "opinion",
    "sitemap",
    "refer",
    "maintenance",
    "free-estimate",
    "opinion-service",
    "energy-review",
    "crew-review",
    "free-estimate/confirmation",
    "survey",
    "privacy-policy",
    "service-area",
    "about-us/real-estate-response-team",
    "book-online"
);

$modulepages = array (
    "opinion",
    "before-after",
    "photo-gallery",
    "refer",
    "meet-the-team",
    "news-and-events",
    "blog",
    "reviews",
    "awards",
    "press-release",
    "crew-review",
    "case-studies",
    "affiliations",
    "technical-papers",
    "case-studies",
    "search",
    "service-area",
    "homeshows",
    "about-us"
);  
 
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    	<meta charset="utf-8">
    	<meta name="viewport" content="width=device-width, initial-scale=1">
    	<title>[[title]]</title>
    	<meta name="description" content="[[description]]">
    	<meta name="referrer" content="no-referrer-when-downgrade">
 
        [[css_head_helper]]
 
        
        <style>
            [[inline_css]]
        </style>

     
     <link rel="stylesheet" href="https://cdn.treehouseinternetgroup.com/cms_core/assets/module-22-test.css?v999">
     <link rel="stylesheet" href="https://cdn.treehouseinternetgroup.com/cms_core/css/new-base-2025.css" />
     <link rel="stylesheet" href="/inc/sb-styles.css">
        
        <!-- City Page CSS Overrides -->
        <?php if ($isCityPage == 1) { ?>
            <style>.citypage_index h1{clear:both;order:-1;grid-row:1;grid-column:1/-1}.citypage_index.module{display:grid;column-gap:2rem}.citypage_main_content{grid-row:2/span 1;grid-column:1}.citypage_index .citypage_sidebar{width:100%;margin-left:0}.citypage_index .widget.widget_citypage_map{margin-bottom:2rem}.widget_citypage_map .widget_content{padding:0}.citypage_index .widget.widget_citypage_map .leaflet-overlay-pane,.leaflet-pane{z-index:1!important}.citypage_index .widget_contact .widget_content{padding:1rem}.citypage_index .widget_contact .widget_content form{width:90%}.citypage_index .contact_form .widget_contact .widget_title{background:var(--brand-dark);padding:1rem .5rem;color:#fff;line-height:1.3;font-family:sans-serif}.reviews_sidebar_widget.widget{clear:both;border-width:0 1px}.citypage_index .widget_contact .widget_content form>div{width:100%;margin-bottom:5px}.citypage_index .widget_contact .widget_content form>div select{height:40px;width:100%}.citypage_index .widget_contact .widget_content form>div label{margin-bottom:3px;display:inline-block;font-family:sans-serif;font-size:13px}.citypage_index .widget_contact .widget_content form label#sms_consent-label{font-weight:400;font-style:normal;font-size:10px}.citypage_index .widget_contact .widget_content form button.submit{padding:.5rem;border-radius:100px;text-transform:uppercase;font-family:sans-serif;font-weight:600}.widget_title{background-color:var(--brand-dark);color:#fff;text-align:center;padding:1rem}.citypage_sidebar .reviews_sidebar_widget.widget .stars{display:flex;margin-bottom:5px}.citypage_sidebar .reviews_sidebar_widget li{margin:0;font-size:14px;line-height:1.3}.citypage_index .reviews_sidebar_widget .widget_items ul .text{margin-top:.5rem;font-style:italic}.citypage_sidebar .widget_services .widget_content{height:150px;overflow-y:scroll}.citypage_sidebar .widget{margin-bottom:1rem}.citypage_sidebar .contact_form.page_widget.us{margin-bottom:0}.citypage_sidebar .widget_awards .widget_thumbnail{width:60px;grid-column:1/3;padding:.5rem 0}.citypage_sidebar .widget_awards .widget_item{display:grid;grid-template-columns:repeat(6,1fr);padding:0 0 .75rem;margin:0 auto .75rem;border-bottom:1px solid #d9d9d9}.citypage_sidebar .widget_awards .widget_item_title{grid-column:3/-1;display:flex;align-items:center;font-size:14px;line-height:1.3}.citypage_sidebar .widget_awards .widget_preview{grid-column:1/-1}.citypage_index .widget_contact .widget_content form button.submit{width:100%}@media screen and (min-width:1024px){.citypage_index.module{display:grid;grid-template-columns:1fr 250px;column-gap:2rem}.citypage_main_content{grid-row:2/span 1;grid-column:1}.citypage_index .citypage_sidebar{grid-row:2;grid-column:2;width:250px}}</style>
        <?php
        }
        ?>
        
 
 

</head>
<body>
<!-- === 1. ATB Header === -->
  <header id="header" class="header__style2">
    <div id="header--logo">
        <a href="/" title="[company]">
            <img src="https://cdn.treehouseinternetgroup.com/cms_core/images/branding/bs/bs_logo_new.svg">
        </a>
    </div>
    <div id="header--territory">
        <p id="header--phone-text">
            <img src="https://cdn.treehouseinternetgroup.com/cms_images/80/icon-call-pink.svg" alt="Phone number">
            <a href="tel:<?php echo $phonenumber; ?>">[phone]</a>
        </p>
        <p id="header--serving-text">Proudly Serving <span>[territory]</span></p>
    </div>
    <div id="header--phone-mobile">
      <p>
        <img src="https://cdn.treehouseinternetgroup.com/cms_images/80/icon-call-pink.svg" alt="Phone number">
        <a href="tel:<?php echo $phonenumber; ?>">[phone]</a>
    </p>
    </div>
    <div id="header--nav">
    <!-- SUPER NAV TOOL -->
        [[top_nav]]
    <!-- END SUPER NAV TOOL -->
    </div>
  </header>
  <!-- === end: 1. ATB Header === -->
<?php if ($thePage == "index") { ?>
  
        <?php
        }
        else
        {
        ?>
        <div id="page-wrap">
            <?php if ( (!in_array($thePage, $fullpage)) && ($isCityPage == 0) ) { ?>  
                <div id="siloBanner">
                    <img src=
                        <?php
                            if (stristr($thePage,"basement-waterproofing"))
                            {
                                ?>
                                 "https://cdn.treehouseinternetgroup.com/core/images/templates/bambam/images/headers/waterproofing-silo-grey.jpg"
                            <?php
                            }
                            elseif (stristr($thePage,"foundation-repair"))
                            {
                                ?>
                                 "https://cdn.treehouseinternetgroup.com/core/images/templates/bambam/images/headers/wall-crack-silo-grey.jpg"
                            <?php
                            }
                            else
                            {
                                ?>
                                "https://cdn.treehouseinternetgroup.com/core/images/templates/bambam/images/headers/about-silo-grey.jpg"
                        <?php
                        }
                        ?>
                    alt="<?php echo $cmsPageData['page.name']; ?>" /><!-- end #siloBanner img -->	
                    <p>
                        <?php echo $cmsPageData['page.name']; ?>
                    </p>
                </div><!-- end #siloBanner -->
   
                    <div id="silo-sidebar">
                        <div id="sidebar-nav">[[single_silo_nav]]</div>
                    </div>
                    <div id="content-wrap">
            <?php
                }
            else
            {
                ?>
                    <div id="content-wrap" class="full-width">
                <?php
                }
                ?>
            
                [[breadcrumbs]]
        <?php
        }
        ?>
    
        
                [[content]]
                           
        <?php if ($thePage != "index") { ?>
            </div><!-- end #content-wrap for child pages -->
        <?php
        }
        ?>
        </div><!-- end #page-wrap for child pages -->
        
        <?php if ( ($thePage != "service-area") && ($isCityPage == 0) ) { ?>
             
        <?php
        }
        ?>
            
         <!-- === 2. ATB Footer === -->
  <footer>
    <div class="container">
      <div id="footer-nav-contact">
        <a
          href="/free-estimate.html"
          class="button btn-pink"
          contenteditable="false"
          style="cursor: pointer"
        >
          GET YOUR FREE ESTIMATE
          <img
            src="https://cdn.treehouseinternetgroup.com/cms_images/80/btn-chevron-right.svg"
          />
        </a>
        <span>Or call us at</span>
        <a href="tel:<?php echo $phonenumber; ?>">[phone]</a>
        <p class="copy"><span>&copy; <? echo date('Y'); ?> [[company]]</span></p>
        [[social_footer]]
        <p class="privacy">
          <a href="/privacy-policy.html" title="Privacy Policy">Privacy Policy</a>
          | <a href="/terms-of-use.html" title="Terms of Use">Terms of Use</a> |
          <a href="/sitemap.html" title="Sitemap">Sitemap</a>
        </p>
      </div>
      <div class="footer-nav-links">[[footer_nav]]</div>
    </div>
    <div id="addresses">
      <p>
        [[address street]], [[address city]], [[address state]] [[address zip]]
      </p>
    </div>
  </footer>
  <!-- === mobile-1. Mobile Fixed Footer === -->
  <nav class="fixed-footer-nav" aria-label="Quick actions">
      <a class="fixed-footer-nav__item" href="/about-us/photo-gallery.html" title="Photo Gallery">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect x="3" y="5" width="18" height="14" rx="2"/>
          <circle cx="9" cy="10" r="1.5"/>
          <path d="M3 16l5-5 4 4 3-3 6 6"/>
        </svg>
        Photos
      </a>
      <a class="fixed-footer-nav__item" href="about-us/reviews.html" title="Customer Reviews">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M5,3.5h14c1.1,0,2,.9,2,2v10c0,1.1-.9,2-2,2H7.39l-4.39,3V5.5c0-1.1.9-2,2-2Z"/>
          <polygon fill="currentColor" stroke-width="1" points="12.12 6.64 13.07 9.55 16.12 9.55 13.65 11.34 14.59 14.25 12.12 12.45 9.65 14.25 10.6 11.34 8.12 9.55 11.18 9.55 12.12 6.64"/>
        </svg>
        Reviews
      </a>
      <div class="fixed-footer-nav__call">
        <a href="tel:<?php echo $phonenumber; ?>" aria-label="Call now" title="Call Now">
          <span class="ring"></span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>
          </svg>
        </a>
      </div>

      <a class="fixed-footer-nav__item" href="/service-area.html" title="Service Area">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/>
          <circle cx="12" cy="9.5" r="2.3"/>
        </svg>
        Service Area
      </a>

      <a class="fixed-footer-nav__item" href="/free-estimate.html" title="Get a Free Estimate">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect x="3" y="5" width="18" height="16" rx="2"/>
          <path d="M3 9h18M8 3v4M16 3v4"/>
          <path d="M9 14l2 2 4-4"/>
        </svg>
        Free Estimate
      </a>
    </nav>
  <!-- === end: mobile-1. Mobile Fixed Footer === -->

  <!-- === end: 2. ATB Footer === -->
  <script>
// Sticky Header/Nav
    let scrollpos = window.scrollY
    const pageBody = document.querySelector("body")  
    const header = document.getElementById("header")
    const header_height = header.offsetHeight - 1
    
    const add_class_on_scroll = () => pageBody.classList.add("stuck")
    const remove_class_on_scroll = () => pageBody.classList.remove("stuck")
    
    window.addEventListener('scroll', function() { 
      scrollpos = window.scrollY;
    
      if (scrollpos > header_height) { add_class_on_scroll() }
      else { remove_class_on_scroll() }
    });
</script>
 
 
 


  </body>

</html>