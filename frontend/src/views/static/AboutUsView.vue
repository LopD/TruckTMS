<template>
  <div class="app">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1>RECEIVE A QUOTE WITHIN MINUTES.</h1>
          <h2 style="font-size: 20px;">More than 20 years of experience in gyms and logistics.</h2>
          <!-- <p>Providing reliable delivery services since 2003</p> -->
          <!-- <button class="hero-button">Request a Quote</button> -->
        </div>
      </div>
    </section>

    <!-- Who we are-->
    <div class="who-we-are-container">
      <h1 class="main-title">WHO WE ARE?</h1>
      
      <div class="content-wrapper">
        <div class="text-column">
          <p class="company-description">
            SMART GYM is a trusted, family-owned with over two decades of expertise. Built on a foundation of safety, service, and trust. With a dedicated team of professionals, we continue to enhance our services.
          </p>
          
          <!-- <p class="contact-info">
            Learn more about <a href="/services" class="services-link">our services</a> and create your partnership with us by contacting us at <a href="/contact-us" class="phone-link">+1 (847) 278-7065</a> or sending us an email.
          </p> -->
        
        </div>
        
        <div class="image-column">
        <!-- Placeholder for truck image -->
      </div>
      </div>
    </div>

    <!-- Driver testimonials -->
    <div class="driver-testimonials-container">
    <h1 class="main-title">WHAT OUR EMPLOYEES SAY:</h1>
    
    <div class="testimonials-grid">
      <div class="testimonial-card">
        <div class="profile-image-container">
          <img src="@/assets/static/images/AboutUsView/JamesDWilliams.jpg" alt="James D. Williams" class="profile-image">
        </div>
        
        <h2 class="driver-name">James D. Williams</h2>
        
        <p class="testimonial-text">
          "I have been with SMART GYM since October 26th 2019. A great company to work for. I enjoy working here."
        </p>
      </div>
      
      <div class="testimonial-card">
        <div class="profile-image-container">
          <img src="@/assets/static/images/AboutUsView/ChhabilalPandey.jpg" alt="Chhabilal Pandey" class="profile-image">
        </div>
        
        <h2 class="driver-name">Chhabilal Pandey</h2>
        
        <p class="testimonial-text">
          "I have been working with SMART GYM since 2019. I always have great experience here. Competitive pay. Never have problems with home time. Owner and all other staff are very nice"
        </p>
      </div>
    </div>
  </div>

  </div>
</template>


<style src="@/assets/static/css/hero.css"></style>
<style scoped>
  .hero {
    background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('@/assets/static/images/AboutUsView/HeroBackgroundImg.jpg');
  }
</style>


<style scoped>
.who-we-are-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.main-title {
  font-size: 48px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.content-wrapper {
  display: flex;
  flex-direction: row;
  width: 100%;
  background-color: var(--KMS_Black);
}

.text-column {
  flex: 0.5;
  background-color: var(--KMS_Black);
  color: #fff;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.company-description {
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 30px;
}

.contact-info {
  font-size: 18px;
  line-height: 1.6;
  background-color: var(--KMS_Black);
}

.services-link {
  color: var(--KMS_Red);
  text-decoration: none;
}

.phone-link {
  color: var(--KMS_Red);
  text-decoration: none;
}

.image-column {
  flex: 1;
  background-image: url('@/assets/static/images/AboutUsView/WhoWeAreSideImg.jpg');
  background-size: cover;
  /* background-position: center; */
  background-repeat: no-repeat;
}

@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }
  
  .image-column {
    height: 300px;
    margin-top: 20px;
  }
}
</style>


<style scoped>
.driver-testimonials-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: Arial, sans-serif;
}

.main-title {
  font-size: 48px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 60px;
}

.testimonials-grid {
  display: flex;
  justify-content: space-between;
  gap: 40px;
}

.testimonial-card {
  flex: 1;
  background-color: #f2f2f2;
  border-radius: 10px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.profile-image-container {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 20px;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.driver-name {
  font-size: 24px;
  font-weight: bold;
  color: #a83232;
  margin-bottom: 20px;
}

.testimonial-text {
  font-size: 16px;
  line-height: 1.6;
}

/* Responsive styles */
@media (max-width: 768px) {
  .testimonials-grid {
    flex-direction: column;
  }
  
  .main-title {
    font-size: 36px;
    margin-bottom: 40px;
  }
}
</style>
