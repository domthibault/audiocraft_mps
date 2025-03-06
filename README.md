# AudioCraft
![docs badge](https://github.com/facebookresearch/audiocraft/workflows/audiocraft_docs/badge.svg)
![linter badge](https://github.com/facebookresearch/audiocraft/workflows/audiocraft_linter/badge.svg)
![tests badge](https://github.com/facebookresearch/audiocraft/workflows/audiocraft_tests/badge.svg)

AudioCraft is a PyTorch library for deep learning research on audio generation. AudioCraft contains inference and training code
for two state-of-the-art AI generative models producing high-quality audio: AudioGen and MusicGen.

This fork is focusing on getting the scripts to work locally with MacOS GPUs (MPS). Not all functions are implemented. It is a work in progress for the benefit of the MUS6329X students.


## Installation
AudioCraft requires Python 3.9, PyTorch 2.1.0. To install AudioCraft, you can run the following:

### Installing Homebrew
First things first, you will need Homebrew, a package manager for macOS and Linux. Homebrew will allow us to install the necessary dependencies. If you don't have it installed, you can do so by running the following command in your terminal:
```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Alternatively, you can download the latest Homebrew package from here: https://github.com/Homebrew/brew/releases/tag/4.4.23

### Installing general dependancies
Three packages need to be installed in priority using Homebrew: ffmpeg, openmp and llvm. Here are the commands to install them:

#### ffmpeg
```shell
# Install ffmpeg for your whole computer
brew install ffmpeg
```

#### openmp
```shell
#Install openmp for your whole computer
brew install libomp

#Export the environment variables for the openmp library
export PATH="/opt/homebrew/opt/libomp/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/libomp/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libomp/include"
```

#### llvm
```shell
#Install llvm for your whole computer
brew install llvm

#Export the environment variables for the llvm library
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/llvm/lib"
export CPPFLAGS="-I/opt/homebrew/opt/llvm/include"
```

## Create a folder and copy the repository
Create a folder and a virtual environment to install of all other dependencies. Use the following commands:
```shell
#Clone the repository (get files from GitHub) and, at the same time, create a folder for the project
git clone https://github.com/domthibault/audiocraft_mps.git

#Move into the folder
cd audiocraft_mps 
```

### Create virtual environment
Create a virtual environment to install of all other dependencies. Use the following commands:
```shell
#Create the virtual environment
python3 -m venv venv

#Activate the virtual environment
source venv/bin/activate
```

### Installing project requirements
Now that you have installed Homebrew and the general dependencies, you can install PyTorch. Run the following command:
```shell
#Have wheel installed first
python -m pip install setuptools wheel

# Best to make sure you have torch installed first, in particular before installing xformers.
pip install torch
pip install -r requirements.txt #This will install all the necessary dependencies except xformers, which we will install last.
```
Once the requirements are installed, you can install xformers using the following command:
```shell
#Install xformers
pip install xformers
```
To make sure everything is in place, run the setup.py script
```shell
#Run the setup.py script
python setup.py install 
```
### Testing inference
You'll have to create a Hugging Face account (if you don't already have one). Once create, find in your account settings, the section to create Access Tokens. Create one and keep it handy. You will need it to log in and download models.
```shell
#Connect to Hugging Face using your API key
huggingface-cli login
#You will be asked your Access Token. You can find it in your Hugging Face account settings. 
#If you say (Y)es to the question, the token will be saved for future use.

#Test the inference using AudioGen
python ./demos/test_audiogen.py "Dog barking" --output ./generated_audio
```

## Models

At the moment, AudioCraft contains the training code and inference code for:
* [MusicGen](./docs/MUSICGEN.md): A state-of-the-art controllable text-to-music model.
* [AudioGen](./docs/AUDIOGEN.md): A state-of-the-art text-to-sound model.
* [EnCodec](./docs/ENCODEC.md): A state-of-the-art high fidelity neural audio codec.
* [Multi Band Diffusion](./docs/MBD.md): An EnCodec compatible decoder using diffusion.
* [MAGNeT](./docs/MAGNET.md): A state-of-the-art non-autoregressive model for text-to-music and text-to-sound.
* [AudioSeal](./docs/WATERMARKING.md): A state-of-the-art audio watermarking.
* [MusicGen Style](./docs/MUSICGEN_STYLE.md): A state-of-the-art text-and-style-to-music model.
* [JASCO](./docs/JASCO.md): "High quality text-to-music model conditioned on chords, melodies and drum tracks"


## Training code

AudioCraft contains PyTorch components for deep learning research in audio and training pipelines for the developed models.
For a general introduction of AudioCraft design principles and instructions to develop your own training pipeline, refer to
the [AudioCraft training documentation](./docs/TRAINING.md).

For reproducing existing work and using the developed training pipelines, refer to the instructions for each specific model
that provides pointers to configuration, example grids and model/task-specific information and FAQ.


## API documentation

We provide some [API documentation](https://facebookresearch.github.io/audiocraft/api_docs/audiocraft/index.html) for AudioCraft.


## FAQ

#### Is the training code available?

Yes! We provide the training code for [EnCodec](./docs/ENCODEC.md), [MusicGen](./docs/MUSICGEN.md),[Multi Band Diffusion](./docs/MBD.md) and [JASCO](./docs/JASCO.md).

#### Where are the models stored?

Hugging Face stored the model in a specific location, which can be overridden by setting the `AUDIOCRAFT_CACHE_DIR` environment variable for the AudioCraft models.
In order to change the cache location of the other Hugging Face models, please check out the [Hugging Face Transformers documentation for the cache setup](https://huggingface.co/docs/transformers/installation#cache-setup).
Finally, if you use a model that relies on Demucs (e.g. `musicgen-melody`) and want to change the download location for Demucs, refer to the [Torch Hub documentation](https://pytorch.org/docs/stable/hub.html#where-are-my-downloaded-models-saved).


## License
* The code in this repository is released under the MIT license as found in the [LICENSE file](LICENSE).
* The models weights in this repository are released under the CC-BY-NC 4.0 license as found in the [LICENSE_weights file](LICENSE_weights).


## Citation

For the general framework of AudioCraft, please cite the following.
```
@inproceedings{copet2023simple,
    title={Simple and Controllable Music Generation},
    author={Jade Copet and Felix Kreuk and Itai Gat and Tal Remez and David Kant and Gabriel Synnaeve and Yossi Adi and Alexandre Défossez},
    booktitle={Thirty-seventh Conference on Neural Information Processing Systems},
    year={2023},
}
```

When referring to a specific model, please cite as mentioned in the model specific README, e.g
[./docs/MUSICGEN.md](./docs/MUSICGEN.md), [./docs/AUDIOGEN.md](./docs/AUDIOGEN.md), etc.
