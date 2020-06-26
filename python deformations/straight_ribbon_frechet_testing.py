import mlfd
import numpy as np
import h5py
import preprocess
import ja
import lte
import dmp
import os
import matplotlib.pyplot as plt
import similaritymeasures

data_names = ['Straight_Ribbon']


metric_funx = [similaritymeasures.frechet_dist]

metric_names = ['Frechet']




def my_shape(shape_name):
    #ask user for the file which the playback is for
    #filename = raw_input('Enter the filename of the .h5 demo: ')
    #open the file
    fname = shape_name + '_drawing_demo.h5'
    filename = '../h5 files/' + fname
    hf = h5py.File(filename, 'r')
    #navigate to necessary data and store in numpy arrays
    shape = hf.get(shape_name)
    y_data = np.array(shape.get('y'))
    x_data = np.array(shape.get('x'))
    #close out file
    hf.close()
    return [x_data, y_data]

def main():
    global data_names
    global metric_names
    global metric_funx
    for i in range (len(data_names)):
        for j in range(len(metric_names)):
            metric_name = metric_names[j]
            plt_fpath = 'FOR_PAPER/' + metric_name + '_' + data_names[i] + '/'
            try:
                os.makedirs(plt_fpath)
            except OSError:
                print ("Creation of the directory %s failed" % plt_fpath)
            else:
                print ("Successfully created the directory %s" % plt_fpath)
            [x, y] = my_shape(data_names[i])
            my_mlfd = mlfd.mlfd()
            my_mlfd.add_traj_dimension(x, 'x')
            my_mlfd.add_traj_dimension(y, 'y')
            my_mlfd.add_deform_alg(ja.perform_ja_improved, 'FJA')
            my_mlfd.add_deform_alg(lte.perform_lte_improved, 'LTE')
            my_mlfd.add_deform_alg(dmp.perform_dmp_improved, 'DMP')
            my_mlfd.add_metric(metric_funx[j], type='Frechet', name=metric_name, weight=1.0, is_dissim=True)
            #my_mlfd.create_grid()
            #my_mlfd.deform_traj(plot=False)
            #my_mlfd.calc_metrics(d_sample=True)
            #my_mlfd.save_results(plt_fpath + metric_name + '_' + data_names[i] + '.h5')
            my_mlfd.read_from_h5(plt_fpath + metric_name + '_' + data_names[i] + '.h5')
            my_mlfd.set_up_classifier()
            my_mlfd.svm_region_contour(filepath=plt_fpath)
            #my_mlfd.generate_svm_region(filepath=plt_fpath)
            #my_mlfd.reproduce_at_point(np.array([[x[0][0] + 5, y[0][0] - 5]]), plot=True)
            #my_mlfd.plot_strongest_gradients(mode='save', filepath=plt_fpath)
            #my_mlfd.plot_sim_hmap(mode='save', filepath=plt_fpath)
            offset = 7
            my_mlfd.reproduce_optimal_at_point(np.array([[x[0][0] - offset - 2, y[0][0] + offset]]), plot=True, mode='save', filepath=plt_fpath)
            my_mlfd.svm_region_contour(mode='save', filepath=plt_fpath, plot_point=[x[0][0] - offset - 2, y[0][0] + offset])
            my_mlfd.reproduce_optimal_at_point(np.array([[x[0][0] + offset, y[0][0] - offset]]), plot=True, mode='save', filepath=plt_fpath)
            my_mlfd.svm_region_contour(mode='save', filepath=plt_fpath, plot_point=[x[0][0] + offset, y[0][0] - offset])
     
if __name__ == '__main__':
  main()