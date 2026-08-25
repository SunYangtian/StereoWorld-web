# StereoWorld: Camera-Guided Stereo Video Generation

### [Project Page](https://sunyangtian.github.io/StereoWorld-web/) | [arXiv](https://arxiv.org/abs/2603.17375) | [Code](https://github.com/VAST-AI-Research/StereoWorld) | [Model](https://huggingface.co/Yang-Tian/StereoWorld)

We present StereoWorld, a camera-conditioned stereo world model that jointly learns appearance and binocular geometry for end-to-end stereo video generation. Unlike monocular RGB or RGBD approaches, StereoWorld operates exclusively within the RGB modality, while simultaneously grounding geometry directly from disparity. To efficiently achieve consistent stereo generation, our approach introduces two key designs: (1) a unified camera-frame RoPE that augments latent tokens with camera-aware rotary positional encoding, enabling relative, view- and time-consistent conditioning while preserving pretrained video priors via a stable attention initialization; and (2) a stereo-aware attention decomposition that factors full 4D attention into 3D intra-view attention plus horizontal row attention, leveraging the epipolar prior to capture disparity-aligned correspondences with substantially lower compute. Across benchmarks, StereoWorld improves stereo consistency, disparity accuracy, and camera-motion fidelity over strong monocular-then-convert pipelines, achieving more than 3x faster generation with an additional 5% gain in viewpoint consistency. Beyond benchmarks, StereoWorld enables end-to-end binocular VR rendering without depth estimation or inpainting, enhances embodied policy learning through metric-scale depth grounding, and is compatible with long-video distillation for extended interactive stereo synthesis.

## Citation

If you find this work useful, please consider citing:

```bibtex
@article{sun2026stereo,
  title={Stereo World Model: Camera-Guided Stereo Video Generation},
  author={Sun, Yang-Tian and Huang, Zehuan and Niu, Yifan and Ma, Lin and Cao, Yan-Pei and Ma, Yuewen and Qi, Xiaojuan},
  journal={arXiv preprint arXiv:2603.17375},
  year={2026}
}
```
