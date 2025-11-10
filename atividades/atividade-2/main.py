def get_xy(fileline: str) -> tuple:
    if fileline is None:
        raise ValueError("Linha vazia ao ler coordenada.")
    s = fileline.strip()
    if not s:
        raise ValueError("Linha em branco onde se esperava 'x,y'.")
    parts = [p.strip() for p in s.split(',')]
    if len(parts) != 2:
        raise ValueError(f"Formato inválido de coordenada. ")
    x, y = float(parts[0]), float(parts[1])
    return (x, y)

def read_input(input_path: str):
    try:
        with open(input_path) as f:
            start = get_xy(f.readline())
            goal = get_xy(f.readline())
            num_obs = int(f.readline())
            
            obstacles = []
            
            for _ in range(num_obs):
                num_vertices = int(f.readline())
                obstacle = []
                for _ in range(num_vertices):
                    pos = get_xy(f.readline())
                    obstacle.append(pos)
                    
                obstacles.append(obstacle)
                
    except FileNotFoundError as e:
        print("Arquivo de entrada não encontrado. Certifique-se de que o arquivo existe.")
        raise(e)
    
    except Exception as e:
        print(f"Algo de errado aconteceu. {e}" )
        raise(e)
    
    return start, goal, obstacles    
        
def main():
   
    start, goal, obstacles = read_input('input.txt')
    
    print("======== EXIBINDO START E GOAL ========")
    print(f"{start}, {goal}")

    print("======== EXIBINDO OBSTÁCULOS ========")
    
    for obs in obstacles:
        print(obs)    
        
if __name__ == "__main__":
    main()