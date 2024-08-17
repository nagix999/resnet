# resnet

Deep Residual Learning for Image Recognition 논문을 pytorch로 구현
Resnet 모델 구현의 핵심이 되는 Residual Block(BasicBlock, BottleneckBlock)을 Resnet Architecture를 참고하여 구현
18, 34, 50, 101, 152 Layers 구성(18, 32 - BasicBlock, 50, 101, 152 - BottleneckBlock)

## 논문 설명

-   논문명: Deep Residual Learning for Image Recognition
-   저자: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
-   저널: Computer Vision and Pattern Recognition(CVPR)
-   URL: https://arxiv.org/abs/1512.03385v1

-   핵심 내용

    -   신경망이 더 깊어질수록 성능 저하(degradation problem)가 발생하는 문제가 발생(정확도의 감소, 반대로 training error와 test error는 증가)

        -   이러한 성능 저하는 과적합에 의한 것이 아님
        -   또한, 기울기 소실이나 폭주(Gradient Vanishing/Exploding)의 문제가 아니라, 깊은 신경망에서 옵티마이저가 겪는 최적화 문제임

    -   심층 잔여 학습 프레임워크(Deep Residual Learning Framework) 도입을 제안

        -   F(x) + x 공식으로 나타나는 shortcut connections 를 통해 입력을 해당 계층의 출력에 덧셈 연산을 통해 수행
        -   전체 네트워크는 SGD 역전파를 통해 End-To-End 방식으로 훈련할 수 있음
        -   Solver(optimizer)를 수정하지 않고도 Caffe와 같은 일반적인 라이브러리에서 쉽게 구현할 수 있음

    -   ImageNet 데이터를 학습한 결과, 기본 네트워크(Residual이 적용되지 않은) 18-layer와 50-layer를 비교하였을 때 50-layer에서 성능이 저하되어 18-layer보다 낮은 성능을 보였으나, Residual Learning이 적용된 네트워크는 18-layer보다 50-layer가 더 높은 성능을 보이며 수렴 속도도 더 빠름
        -   34 계층 Resnet은 매우 경쟁력 있는 정확도를 달성했고, 상위 5개의 검증 오차는 4.49%임
        -   152 계층 모델 2개를 결합한 앙상블을 구성하여 ILSVRC 2015에서 1위 입상
