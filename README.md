# Tower Defense Strategy Game

A comprehensive 2D tower defense game built with Python and Pygame featuring advanced AI pathfinding algorithms, multiple tower types, diverse enemy varieties, and progressive difficulty levels.

![Game Demo](https://img.shields.io/badge/Status-Complete-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.5.2-red)

## 🎮 Game Features

### Tower Types
- **Basic Tower** ($50) - Standard damage and range
- **Sniper Tower** ($150) - High damage, long range, slow fire rate
- **Freeze Tower** ($100) - Slows down enemies with ice damage
- **Explosive Tower** ($200) - Area damage to multiple enemies
- **Laser Tower** ($300) - Continuous beam damage

### Enemy Types
- **Basic Enemy** - Standard health and speed
- **Fast Enemy** - Low health but high speed
- **Tank Enemy** - High health but slow movement
- **Flying Enemy** - Medium stats, can fly over obstacles
- **Boss Enemy** - Very high health and moderate speed

### Game Mechanics
- **15 Progressive Waves** with increasing difficulty
- **Dynamic Enemy Spawning** with intelligent AI pathfinding
- **Real-time Strategy** tower placement and resource management
- **Score System** with monetary rewards for eliminations
- **Lives System** - Game over when enemies reach the end

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/simran-dev/tower-defense-game.git
cd tower-defense-game
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the game**
```bash
python tower_defense_game.py
```

## 🕹️ How to Play

### Controls
- **Left Click** - Place selected tower at cursor position
- **Tower Selection** - Click on tower buttons at bottom of screen
- **R Key** - Restart game (when game over or victory)

### Strategy Tips
1. **Early Game**: Start with Basic towers to establish defense
2. **Mid Game**: Upgrade to Sniper towers for high-value targets
3. **Late Game**: Use Explosive and Laser towers for crowd control
4. **Resource Management**: Balance tower purchases with upgrade timing
5. **Path Blocking**: Strategic placement to maximize enemy exposure

### Scoring System
- Basic Enemy: 10 points
- Fast Enemy: 15 points  
- Tank Enemy: 25 points
- Flying Enemy: 20 points
- Boss Enemy: 100 points

## 🏗️ Technical Implementation

### Architecture
- **Object-Oriented Design**: Separate classes for Game, Tower, Enemy
- **Observer Pattern**: Real-time game state updates
- **Factory Pattern**: Dynamic enemy and tower creation
- **State Management**: Centralized game state handling

### Key Algorithms
- **A* Pathfinding**: Intelligent enemy navigation
- **Collision Detection**: Precise projectile-enemy interactions
- **Range Calculation**: Efficient tower targeting system
- **Wave Management**: Progressive difficulty scaling

### Performance Features
- **60 FPS** smooth gameplay
- **Efficient Rendering**: Optimized drawing operations
- **Memory Management**: Proper object cleanup
- **Scalable Architecture**: Easy to add new content

## 📁 Project Structure

```
tower-defense-game/
├── tower_defense_game.py    # Main game file with complete implementation
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── screenshots/            # Game screenshots (optional)
└── assets/                # Game assets (optional)
    ├── sounds/
    └── images/
```

## 🎯 Game Development Features

### Advanced Mechanics Implemented
- **Dynamic Enemy Spawning**: Time-based enemy creation system
- **Multi-target Tower Systems**: Different targeting algorithms per tower type
- **Health Bar Visualization**: Real-time enemy health display
- **Progressive Wave Difficulty**: Adaptive enemy composition
- **Resource Economy**: Balanced money and upgrade system

### Code Quality Features
- **Type Hints**: Full Python type annotation support
- **Modular Design**: Separate classes for game components
- **Error Handling**: Robust game state management
- **Extensible Architecture**: Easy to add new towers/enemies

## 🔧 Customization Options

### Adding New Tower Types
```python
# Add to TowerType enum
class TowerType(Enum):
    YOUR_TOWER = 6

# Add tower stats in Tower.__init__()
TowerType.YOUR_TOWER: {
    "damage": 100, 
    "range": 150, 
    "fire_rate": 800, 
    "cost": 250, 
    "color": (255, 100, 100)
}
```

### Adding New Enemy Types
```python
# Add to EnemyType enum  
class EnemyType(Enum):
    YOUR_ENEMY = 6

# Add enemy stats in Enemy.__init__()
EnemyType.YOUR_ENEMY: {
    "hp": 200, 
    "speed": 2.5, 
    "reward": 30, 
    "color": (100, 255, 100), 
    "size": 18
}
```

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04+
- **Python**: 3.8+
- **RAM**: 2GB
- **Storage**: 50MB

### Recommended Requirements  
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.10+
- **RAM**: 4GB
- **Storage**: 100MB

## 🚀 Future Enhancements

### Planned Features
- [ ] **Sound Effects** and background music
- [ ] **Power-ups** and special abilities
- [ ] **Multiple Maps** with different path layouts  
- [ ] **Tower Upgrades** system with enhanced capabilities
- [ ] **High Score** leaderboard with persistent storage
- [ ] **Multiplayer Mode** for competitive gameplay

### Technical Improvements
- [ ] **Asset Loading** system for graphics and sounds
- [ ] **Configuration Files** for easy game balancing
- [ ] **Save/Load** game state functionality
- [ ] **Performance Profiling** and optimization
- [ ] **Unit Tests** for core game mechanics

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Simran**
- Email: ss6773568@gmail.com
- GitHub:
- LinkedIn:www.linkedin.com/in/simran-3a4786230

## 🙏 Acknowledgments

- **Pygame Community** for excellent documentation and support
- **Game Development Patterns** from "Game Programming Patterns" by Robert Nystrom
- **Algorithm Implementation** inspired by "Introduction to Algorithms" concepts
- **Open Source Contributors** who make game development accessible

---

⭐ **Star this repository if you found it helpful!** ⭐
