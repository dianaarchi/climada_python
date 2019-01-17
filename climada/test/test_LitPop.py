"""
This file is part of CLIMADA.

Copyright (C) 2017 CLIMADA contributors listed in AUTHORS.

CLIMADA is free software: you can redistribute it and/or modify it under the
terms of the GNU Lesser General Public License as published by the Free
Software Foundation, version 3.

CLIMADA is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with CLIMADA. If not, see <https://www.gnu.org/licenses/>.

Tests on LitPop exposures.
"""

import unittest
import numpy as np

from climada.entity.exposures.litpop import LitPop
from climada.util.finance import world_bank_wealth_account

# ---------------------
class TestDefault(unittest.TestCase):
    """Test data availability checks (blackmarble nightlight and gpw population):"""

    def test_switzerland300_pass(self):
        """Create LitPop entity for Switzerland on 300 arcsec:"""
        country_name = ['CHE']
        resolution = 300
        ent = LitPop()
        with self.assertLogs('climada.entity.exposures.litpop', level='INFO') as cm:
            ent.set_country(country_name, res_arcsec=resolution)
        # print(cm)
        self.assertIn('Generating LitPop data at a resolution of 300 arcsec', cm.output[0])
        self.assertTrue(ent.region_id.min() == 756)
        self.assertTrue(ent.region_id.max() == 756)
        self.assertTrue(ent.value.sum() == 3343726398022.6606)

    def test_switzerland30_pass(self):
        """Create LitPop entity for Switzerland on 30 arcsec:"""
        country_name = ['CHE']
        resolution = 30
        ent = LitPop()
        with self.assertLogs('climada.entity.exposures.litpop', level='INFO') as cm:
            ent.set_country(country_name, res_arcsec=resolution, reference_year=2016)
        # print(cm)
        self.assertIn('Generating LitPop data at a resolution of 30 arcsec', cm.output[0])
        self.assertTrue(ent.region_id.min() == 756)
        self.assertTrue(ent.region_id.max() == 756)
        self.assertTrue(ent.value.sum() == 3343726398022.672)

    def test_suriname30_nfw_pass(self):
        """Create LitPop entity for Suriname for non-finanical wealth:"""
        country_name = ['SUR']
        fin_mode = 'nfw'
        ent = LitPop()
        with self.assertLogs('climada.entity.exposures.litpop', level='INFO') as cm:
            ent.set_country(country_name, reference_year=2016, fin_mode=fin_mode)
        # print(cm)
        self.assertIn('Generating LitPop data at a resolution of 30.0 arcsec', cm.output[0])
        self.assertTrue(ent.region_id.min() == 740)
        self.assertTrue(ent.region_id.max() == 740)
        self.assertTrue(ent.value.sum() == 2414756959.8304553)

    def test_switzerland300_pc2016_pass(self):
        """Create LitPop entity for Switzerland 2016 with admin1 and produced capital:"""
        country_name = ['CHE']
        fin_mode = 'pc'
        resolution = 300
        ref_year = 2016
        adm1 = True
        cons = True
        _, comparison_total_val = world_bank_wealth_account(country_name[0], ref_year, \
                                                                no_land=1)
        ent = LitPop()
        with self.assertLogs('climada.entity.exposures.litpop', level='INFO') as cm:
            ent.set_country(country_name, res_arcsec=resolution, \
                            reference_year=ref_year, fin_mode=fin_mode, \
                            conserve_cntrytotal=cons, calc_admin1=adm1)
        # print(cm)
        self.assertIn('Generating LitPop data at a resolution of 300 arcsec', cm.output[0])
        self.assertTrue(np.around(ent.value.sum(),0) == np.around(comparison_total_val,0))
        self.assertTrue(ent.value.sum() == 2217353764117.5)

    def test_switzerland300_pc2013_pass(self):
        """Create LitPop entity for Switzerland 2013 for produced capital:"""
        country_name = ['CHE']
        fin_mode = 'pc'
        resolution = 300
        ref_year = 2013
        _, comparison_total_val = world_bank_wealth_account(country_name[0], ref_year, no_land=1)
        ent = LitPop()
        with self.assertLogs('climada.entity.exposures.litpop', level='INFO') as cm:
            ent.set_country(country_name, res_arcsec=resolution, \
                            reference_year=ref_year, fin_mode=fin_mode)
        # print(cm)
        self.assertIn('Generating LitPop data at a resolution of 300 arcsec', cm.output[0])
        self.assertTrue(ent.value.sum() == comparison_total_val)
        self.assertTrue(ent.value.sum() == 2296358085749.2)

# Execute Tests
TESTS = unittest.TestLoader().loadTestsFromTestCase(TestDefault)
unittest.TextTestRunner(verbosity=2).run(TESTS)