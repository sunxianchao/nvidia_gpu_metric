# nvidia_gpu_metric
由于线上容器不方便依赖第三方库，因此没有使用pynvml作为获取gpu信息的模块
通过python解析nvidia-smi 命令监控 gpu 该方案不依赖第三方库

## 1.获取nvidia-smi输出的结果转换成xml
nvidia-smi -q -x

## 2. 通过xml.tree解析所需要的节点

## 3. 安装监控的格式打印数据
