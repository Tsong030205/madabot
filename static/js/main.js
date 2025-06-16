        // Mobile menu toggle
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
        
        // Carousel functionality
        const carouselItems = document.querySelectorAll('.carousel-item');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const indicators = document.querySelectorAll('.carousel-indicator');
        
        let currentIndex = 0;
        
        function showSlide(index) {
            // Hide all slides
            carouselItems.forEach(item => {
                item.classList.remove('opacity-0');
                item.classList.add('opacity-0');
            });
            
            // Show current slide
            carouselItems[index].classList.remove('opacity-0');
            
            // Update indicators
            indicators.forEach((indicator, i) => {
                if (i === index) {
                    indicator.classList.remove('bg-opacity-50');
                    indicator.classList.add('bg-opacity-100');
                } else {
                    indicator.classList.remove('bg-opacity-100');
                    indicator.classList.add('bg-opacity-50');
                }
            });
            
            currentIndex = index;
        }
        
        function nextSlide() {
            let newIndex = (currentIndex + 1) % carouselItems.length;
            showSlide(newIndex);
        }
        
        function prevSlide() {
            let newIndex = (currentIndex - 1 + carouselItems.length) % carouselItems.length;
            showSlide(newIndex);
        }
        
        // Set up event listeners
        nextBtn.addEventListener('click', nextSlide);
        prevBtn.addEventListener('click', prevSlide);
        
        indicators.forEach(indicator => {
            indicator.addEventListener('click', () => {
                showSlide(parseInt(indicator.dataset.index));
            });
        });
        
        // Auto-advance carousel
        let carouselInterval = setInterval(nextSlide, 5000);
        
        function resetInterval() {
            clearInterval(carouselInterval);
            carouselInterval = setInterval(nextSlide, 5000);
        }
        
        nextBtn.addEventListener('click', resetInterval);
        prevBtn.addEventListener('click', resetInterval);
        indicators.forEach(indicator => {
            indicator.addEventListener('click', resetInterval);
        });
        
        // Show first slide initially
        showSlide(0);
        
        // Back to top button
        const backToTopButton = document.getElementById('back-to-top');
        
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.remove('opacity-0', 'invisible');
                backToTopButton.classList.add('opacity-100', 'visible');
            } else {
                backToTopButton.classList.remove('opacity-100', 'visible');
                backToTopButton.classList.add('opacity-0', 'invisible');
            }
        });
        
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                    
                    // Close mobile menu if open
                    if (!mobileMenu.classList.contains('hidden')) {
                        mobileMenu.classList.add('hidden');
                    }
                }
            });
        });
        
        // Animation on scroll
        function animateOnScroll() {
            const elements = document.querySelectorAll('.animate-fade-in');
            
            elements.forEach(element => {
                const elementPosition = element.getBoundingClientRect().top;
                const screenPosition = window.innerHeight / 1.3;
                
                if (elementPosition < screenPosition) {
                    element.classList.add('opacity-100');
                }
            });
        }
        
        // Initially hide all animate-fade-in elements
        document.querySelectorAll('.animate-fade-in').forEach(el => {
            el.classList.add('opacity-0');
        });
        
        window.addEventListener('scroll', animateOnScroll);
        window.addEventListener('load', animateOnScroll);


// Chatbot functionality
const chatbotContainer = document.getElementById('chatbot-container');
const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const languageSelect = document.getElementById('language');

chatbotToggle.addEventListener('click', () => {
    chatbotContainer.classList.toggle('hidden');
});

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `p-2 mb-2 rounded text-sm ${isUser ? 'bg-amber-100 text-right' : 'bg-gray-200 text-left text-gray-800'}`;
    messageDiv.innerHTML = content; // Utiliser innerHTML pour gérer les liens
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    const language = languageSelect.value;
    if (!message) return;

    addMessage(message, true);
    userInput.value = '';

    try {
        const response = await fetch('/api/chatbot/response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ message, language }),
        });
        const data = await response.json();
        addMessage(data.answer);
    } catch (error) {
        addMessage("Erreur de connexion au serveur.");
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

addMessage("Bienvenue ! Posez vos questions sur vos voyages à Madagascar ou tapez 'réserver' pour commencer une réservation.");