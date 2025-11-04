<template>
  <div class="app">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1>SMART GYM INC.</h1>
          <h2>Your Trusted Partner</h2>
          <p>Providing reliable services since 2003</p>
          <button class="hero-button">Request a Quote</button>
        </div>
      </div>
    </section>

    <!-- Service section -->
    <!-- <section class="services">
      <div class="container">
        <h2 class="section-title">OUR SERVICES</h2>
        <div class="service-grid">
          <div class="service-card">
            <img 
              src="@/assets/static/images/HomeView/ServicesIconsCombined.png" 
              style="width: 110px; height: 115px; object-fit: none; object-position: -280px -0px;" 
              alt="Partial image"
            />
            <h3 >Otr/regional shipping</h3>
            <p >Transport everything you need safe and fast, all across the country.</p>
          </div>
          <div class="service-card">
            <img 
              src="@/assets/static/images/HomeView/ServicesIconsCombined.png" 
              style="width: 155px; height: 115px; object-fit: none; object-position: -110px -0px;" 
              alt="Partial image"
            />
            <h3>High-value freight </h3>
            <p>Secure every kind of high-value luggage and electronics with our trucks.</p>
          </div>
          <div class="service-card">
            <img 
              src="@/assets/static/images/HomeView/ServicesIconsCombined.png" 
              style="width: 155px; height: 115px; object-fit: none; object-position: -700px -0px;" 
              alt="Partial image"
            />
            <h3>cross-docking/ warehousing </h3>
            <p>Ensure faster, but safe storage of your products at any time with our warehousing.</p>
          </div>
          <div class="service-card">
            <img 
              src="@/assets/static/images/HomeView/ServicesIconsCombined.png" 
              style="width: 155px; height: 115px; object-fit: none; object-position: -560px -0px;" 
              alt="Partial image"
            />
            <h3>refrigerated FREIGHT</h3>
            <p>Transport food and other products with precise control over temperature.</p>
          </div>
          <div class="service-card">
            <img 
              src="@/assets/static/images/HomeView/ServicesIconsCombined.png" 
              style="width: 155px; height: 115px; object-fit: none; object-position: -400px -0px;" 
              alt="Partial image"
            />
            <h3>dry FREIGHT</h3>
            <p>Make safe and flexible transport solutions for all kinds of goods.</p>
          </div>
          <div class="service-card">
            <img 
              src="@/assets/static/images/HomeView/ServicesIconsCombined.png" 
              style="width: 110px; height: 115px; object-fit: none; object-position: -0px -0px;" 
              alt="Partial image"
            />
            <h3>hazmat FREIGHT</h3>
            <p>Ensure the next transportation of hazardous materials, such as chemicals.</p>
          </div>
        </div>
      </div>
    </section> -->

    <!-- About Section -->
    <section class="about">
      <div class="container">
        <div class="about-content">
          <div class="about-image">
            <div class="about-text">
              <h2 class="section-title about-title">ABOUT SMART GYM</h2>
              <p>SMART GYM is a family-owned business with over 20 years of experience. At SMART GYM, we build long-term relationships with our clients by delivering safe, flexible, and timely solutions for all their needs.</p>
              <!-- <button class="cta-button secondary">Learn More</button> -->
              <router-link to="/about-us" class="cta-button secondary">Learn More</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- <section>
      <ContactInfoWithMap :markerPosition="[42.054697522390306, -88.04709147821316]" :zoom="10" /> 
    </section> -->

    
  </div>
</template>

<script>
// import ContactInfoWithMap from '@/components/ContactInfoWithMap.vue';

export default {
  name: 'HomeView',
  components: {
    // ContactInfoWithMap,
  }
}
</script>

<style src="@/assets/static/css/hero.css"></style>
<style scoped>
  .hero {
    background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),url('@/assets/static/images/HomeView/LearnMoreBackgroundImg.jpg');
  }
</style>

<style >
/* Global Styles */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Arial', sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-title {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
  font-size: 32px;
  position: relative;
  padding-bottom: 15px;
}

.section-title.about-title {
  text-align: center;
  margin-bottom: 40px;
  color: white;
  font-size: 32px;
  position: relative;
  padding-bottom: 15px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background-color: #e63946;
}

.cta-button {
  background-color: var(--KMS_Red);
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background-color: #c1121f;
}

.cta-button.secondary {
  background-color: var(--KMS_Red);
}

.cta-button.secondary:hover {
  background-color: var(--KMS_BrightRed);
}

/* About Section */
.about {
  padding: 80px 0;
}

.about-content {
  display: flex;
  align-items: center;
  gap: 40px;
}

.about-text {
  flex: 1;
  color: white;
}

.about-text p {
  margin-bottom: 20px;
  line-height: 1.6;
}

.about-image {
  /* flex: 1; */

  /* background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('@/assets/static/images/HomeView/AboutUsBackgroundImg.webp'); */
  background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('@/assets/static/images/HomeView/AboutUsBackgroundImg.jpg');
  background-size: cover;
  background-position: center;
  height: 80vh;
  display: flex;
  align-items: center;
  color: white;
  text-align: center;
  padding-top: 80px;
}

.about-image img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Contact Section */
.contact {
  padding: 80px 0;
}

.contact-content {
  display: flex;
  gap: 40px;
}

.contact-form {
  flex: 2;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group textarea {
  height: 150px;
  resize: vertical;
}

.contact-info {
  flex: 1;
  background-color: #1d3557;
  padding: 30px;
  border-radius: 8px;
  color: white;
}

.contact-info h3 {
  margin-bottom: 20px;
  border-bottom: 2px solid #e63946;
  padding-bottom: 10px;
}

.contact-info p {
  margin-bottom: 10px;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .nav-links {
    display: none; /* In a real implementation, you'd add a mobile menu */
  }
  
  .about-content,
  .contact-content {
    flex-direction: column;
  }
  
  .hero-content h1 {
    font-size: 36px;
  }
  
  .hero-content h2 {
    font-size: 24px;
  }
}
</style>

<style scoped>
/* Services Section */
.services {
  padding: 80px 0;
  background-color: #f8f9fa;
}

.service-grid {
  display: grid;
  /* grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); */
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.service-card {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.service-card:hover {
  transform: translateY(-10px);
}

.service-card img {
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}

.service-card h3 {
  margin-bottom: 15px;
  padding-bottom: 5px;
  font-size: 26px;
  font-weight:800;
  text-transform: uppercase;
  color: #1d3557;
}

</style>