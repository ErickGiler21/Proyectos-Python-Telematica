# Proyectos Python para Telemática y Redes  
**Erick Giler Veintimilla** – Egresado en Ingeniería Telemática

Portafolio de herramientas desarrolladas en Python para aplicaciones en redes, telecomunicaciones, GIS y fibra óptica.

### Proyectos incluidos

1. **TelematicaTools.py**  
   Suite integrada para:  
   - Monitoreo de latencia de red (ping múltiple a DNS)  
   - Optimización de rutas de fibra óptica  
   - Validación y limpieza de datos GIS (CSV)  

2. **FiberNetworkPlanner.py**  
   Planificador de redes de fibra:  
   - Carga/agrega nodos con coordenadas GPS  
   - Ruta óptima (greedy) + cálculo de costos  
   - Mapa interactivo con folium (marcadores + líneas + zonas de cobertura)  

3. **TrafficSimulatorAnalyzer.py**  
   Simulador de tráfico en redes:  
   - Modelo Poisson para llegadas de paquetes  
   - Cálculo de latencia, congestión, pérdidas y throughput  
   - Gráficos de evolución y reportes CSV/TXT  

4. **NetworkInventoryManager.py**  
   Gestor de inventario de equipos de telecomunicaciones:  
   - Agregar, editar, eliminar, buscar y listar  
   - Persistencia en JSON + reportes  

### Tecnologías usadas
- Python 3  
- pandas, numpy, matplotlib  
- geopy, folium  
- ping3  
- json, os, datetime  

### Cómo probarlos
1. Clona el repositorio:
   ```bash
   git clone https://github.com/ErickGiler21/Proyectos-Python-Telematica.git
   cd Proyectos-Python-Telematica