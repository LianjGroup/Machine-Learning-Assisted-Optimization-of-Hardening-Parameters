# Machine Learning Assisted Prediction of Hardening Parameters 

Hardening parameters play a crucial role in materials science and engineering, representing the response of a material to deformation and stress. In this project, we leverage the power of machine learning, specifically neural networks, to predict hardening parameters. 

![inverse_2](https://github.com/Crista96/coeproject3/assets/85801775/474f1875-3344-4bdc-bbf5-e34d9dad2161)

<sub> Figure Source: R. Lourenço, A. Andrade-Campos, and P. Georgieva, “The use of machine-learning techniques in material constitutive modelling for metal forming processes,” Metals, vol. 12, no. 3, p. 427, 2022.</sub>

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development purposes.

### Prerequisites

In order to run and visualise the main model, you need to have the following libraries installed:

- PyTorch
- NumPy
- Pandas
- scikit-learn 
- scikit-neuralnetwork (skorch)
- Matplotlib
- xgboost

### Installation

1. Clone the repository to your local device by forking it and then open the code in your preferred local environment. 

2. If you don't have the necessary libraries specified in the prerequisites section, open the terminal and run 'pip install -r requirements.txt'. 

3. Ensure to tailor the parameter intervals for 'c4' and 'c6' appropriately, especially if the material under consideration differs significantly from DP1000. Adjusting these intervals is crucial for optimizing the model's performance on diverse materials, ensuring accurate predictions and reliable outcomes. Be mindful of the specific characteristics and behavior of the material you are working with to fine-tune the model for optimal results.

4. For seamless execution, the model is implemented within a Jupyter environment. Simply click on the 'run' icon to effortlessly execute the code and witness the model in action. This streamlined setup ensures a user-friendly experience, allowing quick access and execution without the need for complex configurations or installations.

Note: For Step-By-Step instructions where I walk you through how I developed the project, watch these videos:

- Part 4, Using CSC For Simulations:
https://www.loom.com/share/cb0dfd3255be4c96aae214a69a13ba65?sid=2109cdf7-67e7-43b3-a0d7-bdde40c1faf4

- Part 3, Constructing Stress-Strain and Force Displacement Curves: https://www.loom.com/share/c16163ff5fe64d2ea5e4e1a7a876e242?sid=682db7cc-b51e-41f0-8208-7846891d75c3

- Part 2, Exploring Random Forest and XGBoost Models:
https://www.loom.com/share/063f10f9a9fe4b84a0b1053f33fc2405?sid=82ecc3ae-28d4-425d-af05-0dff60732cb7

- Part 1, Neural Network Model Walkthrough: 
https://www.loom.com/share/6b575915aaa44bee87e54fdb092187c7?sid=06ffb9ae-697d-40e8-b063-23f654a6a035

## License

You are welcome to utilize this tool for your personal research or educational endeavors. Feel free to explore its features, experiment with the code, and adapt it to suit your specific needs. We encourage learning, collaboration, and innovation, and hope that this tool proves valuable in your research or educational pursuits.

## Author

Fikri San Koktas - I was responsible for the development of the whole model as a member of Group 3. It has been quite a challenge for me as I didn't have any previous machine learning experience, thus had to learn everything from scracth. Still, I enjoyed the process very much. 

## Acknowledgments

Special acknowledgments to Li Zinan for her invaluable support throughout the entire process. Her continuous feedback, guidance, and provision of essential templates for simulations have significantly contributed to the success of this project. We extend our sincere gratitude for their collaborative spirit and assistance.

Special thanks to Binh for providing invaluable assistance in resolving the challenges associated with pushing large data files to GitHub. 

Gratitude to Professor Junhe Lian for their outstanding efforts in organizing and facilitating the course. 
