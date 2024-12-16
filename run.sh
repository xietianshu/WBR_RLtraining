conda activate wheel_legged
cd ~/Wheel-Legged-Gym
tensorboard --logdir .

python wheel_legged_gym/scripts/train.py --task=wheel_legged --headless
python wheel_legged_gym/scripts/play.py --task=wheel_legged

python wheel_legged_gym/scripts/train.py --task=wheel_legged_rough --headless
python wheel_legged_gym/scripts/play.py --task=wheel_legged_rough

