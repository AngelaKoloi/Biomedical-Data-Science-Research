import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from joypy import joyplot
sns.set(style="darkgrid")
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
from sdv.tabular import GaussianCopula
from sdv.lite import TabularPreset
from sdv.tabular import CTGAN
from sdv.tabular import CopulaGAN
from sdv.tabular import TVAE
from sdv.evaluation import evaluate
import torch
import warnings
warnings.filterwarnings("ignore")
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

class syntheticData:

        def __init__(self,data,sample):
            self.data = data
            self.sample = sample
            self.ks_metrics = dict()
            self.selected_model = dict()
            self.sample_data = pd.DataFrame()

        def gaussian_model(self):
            data = self.data.copy()
            model = GaussianCopula()
            model.fit(data)
            temp = model.sample(self.sample)
            return temp,evaluate(temp, data, metrics=['CSTest', 'KSComplement'], aggregate=False).iloc[1:,3].values

        def tabular_preset(self):
            data = self.data.copy()
            model = TabularPreset(name='FAST_ML')
            model.fit(data)
            temp = model.sample(num_rows=self.sample)
            return temp,evaluate(temp, data, metrics=['CSTest', 'KSComplement'], aggregate=False).iloc[1:,3].values

        def ctgan(self):
            data = self.data.copy()
            model = CTGAN()
            model.fit(data)
            temp = model.sample(num_rows=self.sample)
            return temp,evaluate(temp, data, metrics=['CSTest', 'KSComplement'], aggregate=False).iloc[1:,3].values

        def copula_gan(self):
            data = self.data.copy()
            model = CopulaGAN()
            model.fit(data)
            temp = model.sample(self.sample)
            return temp,evaluate(temp, data, metrics=['CSTest', 'KSComplement'], aggregate=False).iloc[1:,3].values

        def tvae(self):
            data = self.data.copy()
            model = TVAE()
            model.fit(data)
            temp = model.sample(num_rows=self.sample)
            return temp,evaluate(temp, data, metrics=['CSTest', 'KSComplement'], aggregate=False).iloc[1:,3].values

#         def gretel(self):
#             features = self.data.to_numpy()
#             n = features.shape[0]
#             features = features[:(n*1),:].reshape(-1, 1, self.data.shape[1])

#             model = DGAN(DGANConfig(
#             max_sequence_len=features.shape[1],
#             sample_len=1,
#             batch_size=min(1000, features.shape[0]),
#             apply_feature_scaling=True,
#             apply_example_scaling=True,
#             use_attribute_discriminator=True,
#             generator_learning_rate=1e-4,z
#             discriminator_learning_rate=1e-4,
#             epochs=10000,
#             ))

#             model.train_numpy(features, feature_types=[OutputType.CONTINUOUS] * features.shape[2])

        def train_models(self):
            self.gaussian_df,self.ks_metrics['gaussian'] = self.gaussian_model()
            self.tabular_df,self.ks_metrics['tabular'] = self.tabular_preset()
            self.ctgan_df,self.ks_metrics['ctgan'] = self.ctgan()
            self.copulagan_df,self.ks_metrics['copula_gan'] = self.copula_gan()
            self.tvae_df,self.ks_metrics['tvae'] = self.tvae()

        def evaluate(self):
            best_model = max(self.ks_metrics, key=self.ks_metrics.get)
            self.selected_model['best_model'] = best_model
            self.selected_model['ks_score'] = self.ks_metrics[best_model]
            if best_model == 'gaussian':
                self.sample_data = self.gaussian_df
            elif best_model == 'tabular':
                self.sample_data = self.tabular_df
            elif best_model == 'ctgan':
                self.sample_data = self.ctgan_df
            elif best_model == 'copula_gan':
                self.sample_data = self.copulagan_df
            elif best_model == 'tvae':
                self.sample_data = self.tvae_df

class inspectData:

        def __init__(self,original_data,synthetic_data):
            self.original_data = original_data
            self.synthetic_data = synthetic_data

            self.original_data['group'] = 'real'
            self.synthetic_data['group'] = 'virtual'
            self.data_combined = pd.concat([self.original_data,self.synthetic_data],axis=0).reset_index(drop=True)

        def density_histogram(self,columns=None):
            if columns==None:
                for col in self.data_combined.columns[0:len(self.data_combined.columns)-1]:
                    sns.histplot(data=self.data_combined, x=col, hue='group',stat='density', common_norm=False)
                    plt.show()
            else:
                for col in columns:
                    sns.histplot(data=self.data_combined, x=col, hue='group',stat='density', common_norm=False)
                    plt.show()

        def kernel_density(self,columns=None):
            if columns==None:
                for col in self.data_combined.columns[0:len(self.data_combined.columns)-1]:
                    sns.kdeplot(data=self.data_combined, x=col, hue='group', common_norm=False)
                    plt.show()
            else:
                for col in columns:
                    sns.kdeplot(data=self.data_combined, x=col, hue='group', common_norm=False)
                    plt.show()
                    
                    

        def cdf(self,columns=None):
            if columns==None:
                for col in self.data_combined.columns[0:len(self.data_combined.columns)-1]:
                    sns.histplot(data=self.data_combined, x=col, hue='group',bins=len(self.data_combined), stat='density',\
                                 element='step', fill=False, cumulative=True, common_norm=False)
                    plt.show()
            else:
                for col in columns:
                    sns.histplot(data=self.data_combined, x=col, hue='group',bins=len(self.data_combined), stat='density',\
                                 element='step', fill=False, cumulative=True, common_norm=False)
                    plt.show()

        def qq_helper(self,col):
            temp = self.data_combined[col].values
            temp_o = self.data_combined.loc[self.data_combined.group=='real', col].values
            temp_s = self.data_combined.loc[self.data_combined.group=='virtual', col].values

            df_pct = pd.DataFrame()
            df_pct['q_real'] = np.percentile(temp_o, range(100))
            df_pct['q_virtual'] = np.percentile(temp_s, range(100))

            plt.figure(figsize=(12, 6))
            plt.scatter(x='q_virtual', y='q_real', data=df_pct, label='Actual fit');
            sns.lineplot(x='q_virtual', y='q_real', data=df_pct, color='r', label='Line of perfect fit');
            plt.legend()
            plt.title("QQ plot of: "+ col)

        def qq_plot(self,columns=None):
            if columns==None:
                for col in self.data_combined.columns[0:len(self.data_combined.columns)-1]:
                    self.qq_helper(col)
            else:
                for col in columns:
                    self.qq_helper(col)

        def ridgeline_plot(self,columns=None):
            if columns==None:
                for col in self.data_combined.columns[0:len(self.data_combined.columns)-1]:
                    joyplot(self.data_combined, by='group', column=col, \
                            colormap=sns.color_palette("crest", as_cmap=True))
                    plt.title(col)
                    plt.show()
            else:
                for col in columns:
                    joyplot(self.data_combined, by='group', column=col, \
                            colormap=sns.color_palette("crest", as_cmap=True))
                    plt.title(col)
                    plt.show()

        def group_boxplots(self,columns=None):
            if columns==None:
                for col in self.data_combined.columns[0:len(self.data_combined.columns)-1]:
                    sns.boxplot(x='group', y=col, data=self.data_combined.sort_values('group'))
                    plt.title(col)
                    plt.show()
            else:
                for col in columns:
                    sns.boxplot(x='group', y=col, data=self.data_combined.sort_values('group'))
                    plt.title(col)
                    plt.show()

        def group_violin_plots(self,columns=None):
            if columns==None:
                for col in self.data_combined.columns[0:len(self.data_combined.columns)-1]:
                    sns.violinplot(x='group', y=col, data=self.data_combined.sort_values('group'))
                    plt.title(col)
                    plt.show()
            else:
                for col in columns:
                    sns.violinplot(x='group', y=col, data=self.data_combined.sort_values('group'))
                    plt.title(col)
                    plt.show()
