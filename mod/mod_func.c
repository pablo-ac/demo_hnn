#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _IC_reg();
extern void _cadad_reg();
extern void _cagk_reg();
extern void _cal_mig_reg();
extern void _can_mig_reg();
extern void _cat_mig_reg();
extern void _h_kole_reg();
extern void _h_migliore_reg();
extern void _ican_sidi_reg();
extern void _kBK_reg();
extern void _kap_BS_reg();
extern void _kdmc_BS_reg();
extern void _kdr_BS_reg();
extern void _nax_BS_reg();
extern void _savedist_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," IC.mod");
fprintf(stderr," cadad.mod");
fprintf(stderr," cagk.mod");
fprintf(stderr," cal_mig.mod");
fprintf(stderr," can_mig.mod");
fprintf(stderr," cat_mig.mod");
fprintf(stderr," h_kole.mod");
fprintf(stderr," h_migliore.mod");
fprintf(stderr," ican_sidi.mod");
fprintf(stderr," kBK.mod");
fprintf(stderr," kap_BS.mod");
fprintf(stderr," kdmc_BS.mod");
fprintf(stderr," kdr_BS.mod");
fprintf(stderr," nax_BS.mod");
fprintf(stderr," savedist.mod");
fprintf(stderr, "\n");
    }
_IC_reg();
_cadad_reg();
_cagk_reg();
_cal_mig_reg();
_can_mig_reg();
_cat_mig_reg();
_h_kole_reg();
_h_migliore_reg();
_ican_sidi_reg();
_kBK_reg();
_kap_BS_reg();
_kdmc_BS_reg();
_kdr_BS_reg();
_nax_BS_reg();
_savedist_reg();
}
