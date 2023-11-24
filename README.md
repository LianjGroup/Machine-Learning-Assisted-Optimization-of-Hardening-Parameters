# Machine Learning Assisted Prediction of Hardening Parameters 

Hardening parameters play a crucial role in materials science and engineering, representing the response of a material to deformation and stress. In this project, we leverage the power of machine learning, specifically neural networks, to predict hardening parameters. 

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

### Installation

1. Clone the repository to your local device by forking it and then open the code in your preferred local environment. 

2. Ensure to tailor the parameter intervals for 'c4' and 'c6' appropriately, especially if the material under consideration differs significantly from DP1000. Adjusting these intervals is crucial for optimizing the model's performance on diverse materials, ensuring accurate predictions and reliable outcomes. Be mindful of the specific characteristics and behavior of the material you are working with to fine-tune the model for optimal results.

3. For seamless execution, the model is implemented within a Jupyter environment. Simply click on the 'run' icon to effortlessly execute the code and witness the model in action. This streamlined setup ensures a user-friendly experience, allowing quick access and execution without the need for complex configurations or installations.

## License

You are welcome to utilize this tool for your personal research or educational endeavors. Feel free to explore its features, experiment with the code, and adapt it to suit your specific needs. We encourage learning, collaboration, and innovation, and hope that this tool proves valuable in your research or educational pursuits.

## Author

Fikri San Koktas - I was responsible for the development of the whole model as a member of Group 3. It has been quite a challenge for me as I didn't have any previous machine learning experience, thus had to learn everything from scracth. Still, I enjoyed the process very much. 

## Acknowledgments

Special acknowledgments to Li Zinan for her invaluable support throughout the entire process. Her continuous feedback, guidance, and provision of essential templates for simulations have significantly contributed to the success of this project. We extend our sincere gratitude for their collaborative spirit and assistance.

Special thanks to Binh for providing invaluable assistance in resolving the challenges associated with pushing large data files to GitHub. 

Gratitude to Professor Junhe Lian for their outstanding efforts in organizing and facilitating the course. 