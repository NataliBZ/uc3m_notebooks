#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern "C" void _NaTs2_t_reg(void);
extern "C" void _SK_E2_reg(void);
extern "C" void _SKv3_1_reg(void);

extern "C" void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"NaTs2_t.mod\"");
    fprintf(stderr, " \"SK_E2.mod\"");
    fprintf(stderr, " \"SKv3_1.mod\"");
    fprintf(stderr, "\n");
  }
  _NaTs2_t_reg();
  _SK_E2_reg();
  _SKv3_1_reg();
}
