// RUN: quark-opt %s --pass-pipeline="builtin.module(func.func(tosa-to-linalg), quark-autodiff, quark-autodiff-inline-function-call, quark-autodiff-optimise)" | FileCheck %s
!type = tensor<f32>

// CHECK：ml_program.global

func.func @mul(%x : !type, %y : !type) -> !type {
  // CHECK: linalg.generic
  %res = "tosa.mul"(%x, %y) {shift = 0 : i8} : (!type, !type) -> !type
  return %res : !type
}

// CHECK-LABEL: @dmul
// CHECK: indexing_maps = [#map, #map, #map]

