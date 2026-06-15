
const introText = `Acadelytics es la plataforma de análisis académico que ayuda a instituciones y profesionales a tomar decisiones basadas en datos. Controla la gestión escolar, el seguimiento de desempeño, y accede a reportes en tiempo real de forma segura y confiable.`

export function renderHomePage(root: HTMLElement) {
  root.innerHTML = `
    <main class="page page-home">
      <header class="hero-card">
        <div class="hero-header">
          <div>
            <span class="brand">Acadelytics</span>
            <h1>Inteligencia académica para la gestión moderna</h1>
            <p>${introText}</p>
          </div>
          <div id="header-controls" class="header-controls"></div>
        </div>

        <div class="hero-actions">
          <label class="search-input">
            <span>Buscar solución</span>
            <input type="text" value="Optimiza tus procesos educativos con datos reales" readonly />
          </label>
          <div class="hero-buttons">
            <a href="#/login" data-router class="button primary">Iniciar sesión</a>
            <a href="#/register" data-router class="button outline">Registrarse</a>
          </div>
        </div>
      </header>

      <section class="services-section">
        <h2>Nuestros servicios</h2>
        <div class="service-cards">
          <article class="service-card">
            <h3>Análisis de Datos</h3>
            <p>Interpretamos resultados académicos para que los docentes y directivos identifiquen áreas de mejora y oportunidades de progreso.</p>
          </article>
          <article class="service-card">
            <h3>Gestión Académica</h3>
            <p>Centraliza calificaciones, asistencia y comunicación con estudiantes en un solo lugar seguro y fácil de usar.</p>
          </article>
          <article class="service-card">
            <h3>Reportes en Tiempo Real</h3>
            <p>Visualiza el rendimiento educativo al instante y genera informes que respaldan decisiones estratégicas.</p>
          </article>
        </div>
      </section>

      <section class="benefits-section">
        <h2>Por qué elegir Acadelytics</h2>
        <div class="benefits-grid">
          <article class="benefit-card">
            <strong>Decisiones basadas en datos</strong>
            <p>Transforma la información de tu institución en acciones concretas y medibles.</p>
          </article>
          <article class="benefit-card">
            <strong>Seguimiento integral</strong>
            <p>Monitorea el progreso de cada estudiante y de cada clase con seguimiento continuo.</p>
          </article>
          <article class="benefit-card">
            <strong>Planificación futura</strong>
            <p>Define metas académicas con visión y reduce la incertidumbre en la toma de decisiones.</p>
          </article>
          <article class="benefit-card">
            <strong>Gestión eficiente</strong>
            <p>Optimiza tareas administrativas para que el equipo se concentre en lo más importante: enseñar.</p>
          </article>
        </div>
      </section>
    </main>
  `
}
