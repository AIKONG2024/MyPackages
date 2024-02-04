# https://www.tensorflow.org/guide/keras/custom_callback?hl=ko
#v1. 24.02.03 KONG SEONUI
import keras
import numpy as np


# EarlyStopping 뜯어고치기

# monitor: 모니터링 metrics
# overfitting_stop_line : 과적합 되면 멈출 기준
# overfitting_count : 과적합 카운팅 기준
# stop_tranning_value: stop 기준 (잘될 떡잎만 키우기) 튜플형태(epoch, monitoring value) 
#===========================================================================================
#?? fit만 반복을 걸어주면 가중치가 계속 쌓이는 효과가 있음 ==> 가중치 공유 모델 생성이 가능해보임!
#===========================================================================================
class CustomEarlyStoppingAtLoss(keras.callbacks.Callback):
    def __init__(self, patience=0, monitor="loss", overfitting_stop_line=0.0, overfitting_count = 0, stop_tranning_epoch = 0, stop_tranning_value = 0.0, is_log=False):
        super(CustomEarlyStoppingAtLoss, self).__init__()
        self.patience = patience
        self.best_weights = None
        self.monitor = monitor
        self.overfitting_stop_line = overfitting_stop_line
        self.stop_tranning_epoch = stop_tranning_epoch
        self.stop_tranning_value = stop_tranning_value
        self.is_log = is_log
        self.overfitting_count = overfitting_count
    def on_train_begin(self, logs=None):
        self.wait = 0
        self.stopped_epoch = 0
        self.best = np.Inf

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get(self.monitor)
        if self.stop_tranning_epoch > 0 and epoch == self.stop_tranning_epoch and self.best > self.stop_tranning_value:
            self.stopped_epoch = epoch
            self.model.stop_training = True
            self.model.set_weights(self.best_weights)        
        if np.less(current, self.best):
            self.best = current
            self.wait = 0
            self.best_weights = self.model.get_weights()
            if self.is_log:
                print(
                f"""
                🎊🎊🎊{self.monitor} renewaled🎊🎊🎊
                {self.monitor} : {self.best}
                """
                )

        else:
            # overfittiong_escaping 
            bounce_count = 0
            if current > self.overfitting_stop_line :
                if self.overfitting_count > bounce_count:
                    self.wait = self.patience
                bounce_count += 1      
                          
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = epoch
                self.model.stop_training = True
                self.model.set_weights(self.best_weights)

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            print("Epoch %05d: early stopping" % (self.stopped_epoch + 1))
