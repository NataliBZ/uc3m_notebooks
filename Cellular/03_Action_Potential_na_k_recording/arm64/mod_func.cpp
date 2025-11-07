#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _CaDynamics_DC0_reg(void);
extern void _Ca_HVA2_reg(void);
extern void _Ca_LVAst_reg(void);
extern void _Ih_reg(void);
extern void _K_Pst_reg(void);
extern void _K_Tst_reg(void);
extern void _NaTg_reg(void);
extern void _Nap_Et2_reg(void);
extern void _SK_E2_reg(void);
extern void _SKv3_1_reg(void);
extern void _TTXDynamicsSwitch_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/CaDynamics_DC0.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/Ca_HVA2.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/Ca_LVAst.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/Ih.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/K_Pst.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/K_Tst.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/NaTg.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/Nap_Et2.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/SK_E2.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/SKv3_1.mod\"");
    fprintf(stderr, " \"4846377e-b403-4fa8-bfd3-9b95506f9dc3/mechanisms/TTXDynamicsSwitch.mod\"");
    fprintf(stderr, "\n");
  }
  _CaDynamics_DC0_reg();
  _Ca_HVA2_reg();
  _Ca_LVAst_reg();
  _Ih_reg();
  _K_Pst_reg();
  _K_Tst_reg();
  _NaTg_reg();
  _Nap_Et2_reg();
  _SK_E2_reg();
  _SKv3_1_reg();
  _TTXDynamicsSwitch_reg();
}

#if defined(__cplusplus)
}
#endif
