window.SITE_DATA = {
  site: {
    team: "StereoWorld",
    teamShort: "SW",
    tagline: "Camera-Guided Stereo Video Generation",
    logo: "assets/favicon.svg",
    links: [
      { label: "GitHub", href: "https://github.com/VAST-AI-Research/StereoWorld", icon: "github" },
      { label: "arXiv", href: "https://arxiv.org/abs/2603.17375", icon: "arxiv" },
      { label: "HuggingFace", href: "https://huggingface.co/Yang-Tian/StereoWorld", icon: "hf" },
    ],
    footer: {
      note: "StereoWorld project page.",
      credit: "Design inspired by the Nerfies / academic-project-page lineage.",
      contact: "mailto:sunyangtian98@gmail.com",
    },
  },

  home: {
    title: "",
    intro: "Explore the world in stereo with StereoWorld, a model that generates view-consistent stereo videos with camera controls.",
  },

  nav: [
    {
      key: "research",
      label: "Research",
      title: "Research",
      intro: "Peer-reviewed research.",
    },
  ],

  projects: [
    {
      id: "stereo-world",
      title: "Stereo World Model",
      short: "StereoWorld",
      subtitle:"Explore the world in stereo with StereoWorld, a model that generates view-consistent stereo videos with camera controls.",
      venue: "CVPR 2026",
      date: "2026-06",
      thumb: "assets/images/teaser.jpg",
      keywords: ["stereo video", "world model", "camera control", "video generation"],

      authors: [
        { name: "Yang-Tian Sun", url: "https://sunyangtian.github.io/", affil: [1] },
        { name: "Zehuan Huang", url: "https://huanngzh.github.io/", affil: [2], note: "†" },
        { name: "Yifan Niu", url: "https://openreview.net/profile?id=~Yifan_Niu3", affil: [2] },
        { name: "Lin Ma", url: "https://marlinilram.github.io/", affil: [3] },
        { name: "Yan-Pei Cao", url: "https://yanpei.me/", affil: [2] },
        { name: "Yuewen Ma", url: "https://openreview.net/profile?id=~Yuewen_Ma1", affil: [3] },
        { name: "Xiaojuan Qi", url: "https://xjqi.github.io/", affil: [1], note: "✉" },
      ],
      affiliations: [
        "The University of Hong Kong",
        "VAST",
        "ByteDance Pico",
      ],
      authorNotes: "† Project Lead　✉ Corresponding Author",

      links: [
        { label: "arXiv", href: "https://arxiv.org/abs/2603.17375", icon: "arxiv" },
        { label: "Code", href: "https://github.com/VAST-AI-Research/StereoWorld", icon: "github" },
        { label: "Model", href: "https://huggingface.co/Yang-Tian/StereoWorld", icon: "hf" },
      ],

      teaser: {
        src: "assets/videos/demo.mp4",
        caption: "StereoWorld generates camera-guided stereo video from a single RGB image with WASD-style camera controls.",
      },

      abstract: "We introduce StereoWorld, a stereo world model capable of performing exploration " +
          "based on given initial observation, generating view-consistent stereo videos with " +
          "intrinsic geometric understanding. The model supports WASD-style camera controls " +
          "for translation, yaw, and pitch, with both flexible stereo (independent left/right " +
          "camera control) and fixed-baseline stereo modes.",

      sections: [
        {
          type: "figure",
          id: "motivation",
          title: "Motivation",
          body: "<ul>" +
              "<li><strong>Stereo vision</strong> — the dominant perceptual mechanism in many biological systems — provides direct, robust geometric cues to 3D scene structure.</li>" +
              "<li>Compared to RGB-D systems, it avoids producing and stabilizing explicit metric depth maps while retaining strong geometric signals.</li>" +
              "</ul>",
          src: "assets/videos/motivation.mp4",
        },
        {
          type: "figure",
          id: "pipeline",
          title: "Pipeline",
          src: "assets/images/pipeline.jpg",
          caption: "<strong>Illustration of StereoWorld.</strong> Given a pair of stereo images and a conditional camera trajectory, StereoWorld first encodes conditional and noisy video latents from different viewpoints and timesteps using a unified camera–frame RoPE representation. It then performs denoising through a DiT equipped with stereo attention, ultimately producing the final stereo video.",
        },
        {
          type: "gallery",
          id: "stereo-video",
          title: "Fixed-Baseline Stereo",
          columns: 2,
          items: [
            { src: "assets/stereo_video/varied_scene_004_lakeside_balcony_w_j_l_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_006_volcano_crater_dj_wk_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_011_underground_river_arch_w_wl_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_012_floating_islands_dj_wk_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_021_snowy_mountain_road_w_wk_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_022_minimal_gallery_w_j_l_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_028_rice_terraces_dj_wk_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_034_tea_house_window_w_j_l_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_037_northern_lights_cabin_w_wl_wj_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_044_music_studio_w_j_l_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_059_hospital_operating_room_w_j_l_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_067_old_europe_square_w_wl_wj_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_071_glacier_lagoon_w_wl_wj_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_073_children_playroom_w_j_l_demo.mp4" },
            { src: "assets/stereo_video/varied_scene_074_coastal_tunnel_road_w_wk_demo.mp4" },
          ],
        },
        {
          type: "gallery",
          id: "stereo-depth",
          title: "Stereo Depth",
          body: "Each video shows <strong>stereo video (left)</strong> side-by-side with the corresponding <strong>depth estimation (right)</strong>.",
          columns: 2,
          items: [
            { src: "assets/stereo_depth/stereo_video1_with_disp_vis1.mp4" },
            { src: "assets/stereo_depth/stereo_video2_with_disp_vis2.mp4" },
          ],
        },
        {
          type: "gallery",
          id: "flex-demo",
          title: "Flexible Stereo",
          body: "Flexible stereo mode supports independent left/right camera control with four right-camera modes: converging, horizontal offset, depth offset, height offset.",
          columns: 3,
          items: [
            { src: "assets/flex_demo/flex_converging_prompt_00117_demo.mp4", caption: "Converging" },
            { src: "assets/flex_demo/flex_converging_prompt_01290_demo.mp4", caption: "Converging" },
            { src: "assets/flex_demo/flex_converging_prompt_05539_demo.mp4", caption: "Converging" },
            { src: "assets/flex_demo/flex_converging_prompt_09641_demo.mp4", caption: "Converging" },
            { src: "assets/flex_demo/flex_depth_offset_prompt_03814_demo.mp4", caption: "Depth Offset" },
            { src: "assets/flex_demo/flex_depth_offset_prompt_05313_demo.mp4", caption: "Depth Offset" },
            { src: "assets/flex_demo/flex_depth_offset_prompt_02664_demo.mp4", caption: "Depth Offset" },
            { src: "assets/flex_demo/flex_depth_offset_prompt_07517_demo.mp4", caption: "Depth Offset" },
            { src: "assets/flex_demo/flex_height_offset_prompt_02504_demo.mp4", caption: "Height Offset" },
            { src: "assets/flex_demo/flex_height_offset_prompt_02927_demo.mp4", caption: "Height Offset" },
            { src: "assets/flex_demo/flex_height_offset_prompt_04808_demo.mp4", caption: "Height Offset" },
            { src: "assets/flex_demo/flex_height_offset_prompt_08317_demo.mp4", caption: "Height Offset" },
            { src: "assets/flex_demo/flex_horizontal_offset_prompt_03257_demo.mp4", caption: "Horizontal Offset" },
            { src: "assets/flex_demo/flex_horizontal_offset_prompt_04506_demo.mp4", caption: "Horizontal Offset" },
            { src: "assets/flex_demo/flex_horizontal_offset_prompt_06924_demo.mp4", caption: "Horizontal Offset" },
            { src: "assets/flex_demo/flex_horizontal_offset_prompt_08785_demo.mp4", caption: "Horizontal Offset" },
          ],
        },
        {
          type: "gallery",
          id: "ar-distillation",
          title: "Autoregressive Long Video Distillation",
          body: "A 4-step autoregressive student model trained via self-forcing distillation generates extended sequences beyond the single-clip frame budget." +
              "<figure style='margin:1.5rem auto;max-width:50%'>" +
              "<img src='assets/images/distillation.jpg' alt='Distillation' loading='lazy' style='width:100%;display:block'>" +
              "<figcaption style='text-align:center;margin-top:0.5rem;font-size:0.9em;color:var(--text-muted);white-space:nowrap'>Attention mask configuration in distillation process.</figcaption>" +
              "</figure>",
          columns: 2,
          items: [
            { src: "assets/ar_demo/custom_varied_021.mp4" },
            { src: "assets/ar_demo/custom_varied_022.mp4" },
            { src: "assets/ar_demo/custom_varied_059.mp4" },
          ],
        },
        {
          type: "gallery",
          id: "inpaint-demo",
          title: "View Inpainting",
          body: "Given a fixed reference video, generate the corresponding another view. <br> Each clip shows: reference | View 1 | View 2.",
          columns: "2-fixed",
          items: [
            { src: "assets/inpaint_demo/shard_01_teacher_cfg5.0_steps50_0000_seed1_concat.mp4" },
            { src: "assets/inpaint_demo/shard_02_teacher_cfg5.0_steps50_0000_seed1_concat.mp4" },
            { src: "assets/inpaint_demo/shard_02_teacher_cfg5.0_steps50_0009_seed1_concat.mp4" },
            { src: "assets/inpaint_demo/shard_02_teacher_cfg5.0_steps50_0012_seed1_concat.mp4" },
            { src: "assets/inpaint_demo/shard_04_teacher_cfg5.0_steps50_0002_seed1_concat.mp4" },
            { src: "assets/inpaint_demo/shard_04_teacher_cfg5.0_steps50_0003_seed1_concat.mp4" },
          ],
        },
      ],

      bibtex:
        "@article{sun2026stereo,\n" +
        "  title={Stereo World Model: Camera-Guided Stereo Video Generation},\n" +
        "  author={Sun Yang-Tian and Huang Zehuan and Niu Yifan and Ma Lin and Cao Yan-Pei and Ma Yuewen and Qi Xiaojuan},\n" +
        "  journal={arXiv preprint arXiv:2603.17375},\n" +
        "  year={2026}\n" +
        "}",

      acknowledgements: "The website template is borrowed from <a href='https://nerfies.github.io/'>Nerfies</a>.",
    },
  ],

  posts: [],
};
