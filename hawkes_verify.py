# a verification script using tick that may help with checking that our code matches with a library

from tick.hawkes import SimuHawkesExpKernels, HawkesExpKern
import numpy as np
import ast

np.set_printoptions(suppress=True)
np.set_printoptions(threshold=np.nan)

decays = 0.01

class hawkes_verify:

    def simulate(self):
        n_nodes = 1
        baseline = [0.1]
        adjacency = [[0.1]]

        end_time = 10000
        # max_jumps=1000;
        a_sim = SimuHawkesExpKernels(adjacency, decays, baseline=baseline, end_time=end_time, verbose=True)
        a_sim.track_intensity(0.01)

        a_sim.simulate()
        # print(a_sim.timestamps)

        # print('Tracked intensity: ', a_sim.tracked_intensity)


        with open('sample_timestamps.txt', 'w') as f:
            f.write(str(list(a_sim.timestamps[0])))

    def learn(self, timestamps):
        gofit = 'least-squares'
        penalty = 'l2'
        C = 1e3
        solver = 'bfgs'
        step = None
        tol = 1e-05
        max_iter = 100
        verbose = False
        print_every = 10
        random_state = None
        elastic_net_ratio = 0.95

        a_kernel = HawkesExpKern(decays, gofit=gofit, penalty=penalty, C=C, solver=solver, step=step, tol=tol,
                                 max_iter=max_iter, verbose=verbose, print_every=print_every,
                                 # elastic_net_ratio=elastic_net_ratio,
                                 random_state=random_state)

        timestamps = np.array(timestamps)

        # print(timestamps)

        timestamps_list = []
        timestamps_list.append(timestamps)

        a_kernel.fit(timestamps_list)

        print("No of users: ", a_kernel.n_nodes)
        print("Estimated mu: ", a_kernel.baseline)
        print("Estimated alpha:", a_kernel.adjacency)
        print("Estimated coeffs: ", a_kernel.coeffs)

        likelihood = a_kernel.score(timestamps_list)

        print('Likelihood: ', likelihood)

        print('Negative Log likelihood: ', -np.log(likelihood))

    def main(self):

        self.simulate()

        with open('sample_timestamps.txt', 'r') as f:
            test_timestamps = ast.literal_eval(f.read())


        test_timestamps = np.array(test_timestamps)

        self.learn(test_timestamps)

if __name__ == '__main__':
    hawkes_verify().main()