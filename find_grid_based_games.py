from gym import envs
import gym_gvgai
from games.gvgai_environment import GVGAIEnvironment
import random


if __name__ == "__main__":

    all_envs = envs.registry.all()
    env_ids = [env_spec.id for env_spec in all_envs if env_spec.id.startswith("gvgai")]
    env_ids = list({s.split("-")[1] for s in env_ids})
    if "x" in env_ids:
        env_ids.remove("x")
    if "ghostbuster" in env_ids:
        env_ids.remove("ghostbuster")
    env_ids = sorted(env_ids)

    level = 0
    version = 0

    grid_based_games = []

    for game in env_ids:
        print(game)
        invalid = False
        env = GVGAIEnvironment(game, level, version)
        for l in range(3):
            for i in range(200):
                _, _, _, sso = env.step(random.choice(env.get_actions()))
                for row in sso.origObservationGrid:
                    for cell in row:
                        for obj in cell:
                            if obj["position"]["x"] % 10 == 0 and obj["position"]["y"] % 10 == 0:
                                continue
                            else:
                                invalid = True
                                break
                        if invalid:
                            break
                    if invalid:
                        break
                if invalid:
                    break
            if invalid:
                break
        if not invalid:
            grid_based_games.append(game)
            print(f"grid-based {game}")
        else:
            print(f"not grid-based {game}")
        env.close()

    with open("data/GVGAI/grid-based-games.txt", "w") as file:  # Use file to refer to the file object
        for game in grid_based_games:
            file.write(game + "\n")
