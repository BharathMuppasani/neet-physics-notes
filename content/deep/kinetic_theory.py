"""Deepening layer for the kinetic-theory chapter (Kinetic Theory of Gases).

Adds derivations (pressure from collisions, Mayer's relation, mean free path),
graph reading, standard NEET ratio results, worked examples and extra MCQs to
each section, plus a new section on specific heats of gases.
Numbers use R = 8.31 J/mol K, k_B = 1.38e-23 J/K and g = 10 m/s^2.
Figure curves (Maxwell distribution, C_V of H2) were computed numerically.
"""

FIG_MAXWELL = ('<svg viewBox="0 0 480 275" role="img" aria-label="Maxwell speed distribution at two temperatures, with most probable, average and rms speeds marked on the colder curve"><line x1="40" y1="230" x2="465" y2="230" style="stroke:var(--ink-2);stroke-width:1.5"/><line x1="40" y1="230" x2="40" y2="25" style="stroke:var(--ink-2);stroke-width:1.5"/><text x="460" y="262" font-size="12" text-anchor="end" style="fill:var(--ink)">speed v</text><text x="46" y="26" font-size="12" style="fill:var(--ink)">fraction of molecules per unit speed</text><path d="M40.0 230.0 L41.3 229.9 L42.6 229.7 L43.9 229.4 L45.2 228.9 L46.6 228.3 L47.9 227.6 L49.2 226.7 L50.5 225.7 L51.8 224.6 L53.1 223.4 L54.4 222.0 L55.8 220.5 L57.1 218.9 L58.4 217.2 L59.7 215.4 L61.0 213.4 L62.3 211.4 L63.6 209.2 L64.9 207.0 L66.2 204.6 L67.6 202.2 L68.9 199.6 L70.2 197.0 L71.5 194.3 L72.8 191.6 L74.1 188.7 L75.4 185.8 L76.8 182.8 L78.1 179.8 L79.4 176.7 L80.7 173.6 L82.0 170.5 L83.3 167.3 L84.6 164.0 L85.9 160.8 L87.2 157.5 L88.6 154.2 L89.9 150.9 L91.2 147.5 L92.5 144.2 L93.8 140.9 L95.1 137.6 L96.4 134.3 L97.8 131.0 L99.1 127.7 L100.4 124.5 L101.7 121.3 L103.0 118.1 L104.3 115.0 L105.6 111.9 L106.9 108.9 L108.2 105.9 L109.6 103.0 L110.9 100.1 L112.2 97.3 L113.5 94.6 L114.8 91.9 L116.1 89.4 L117.4 86.9 L118.8 84.4 L120.1 82.1 L121.4 79.8 L122.7 77.6 L124.0 75.6 L125.3 73.6 L126.6 71.7 L127.9 69.9 L129.2 68.2 L130.6 66.5 L131.9 65.0 L133.2 63.6 L134.5 62.3 L135.8 61.1 L137.1 60.0 L138.4 59.0 L139.8 58.1 L141.1 57.4 L142.4 56.7 L143.7 56.1 L145.0 55.6 L146.3 55.2 L147.6 55.0 L148.9 54.8 L150.2 54.7 L151.6 54.8 L152.9 54.9 L154.2 55.1 L155.5 55.4 L156.8 55.8 L158.1 56.3 L159.4 56.9 L160.8 57.6 L162.1 58.4 L163.4 59.2 L164.7 60.2 L166.0 61.2 L167.3 62.3 L168.6 63.5 L169.9 64.7 L171.2 66.0 L172.6 67.4 L173.9 68.8 L175.2 70.3 L176.5 71.9 L177.8 73.5 L179.1 75.2 L180.4 76.9 L181.8 78.7 L183.1 80.5 L184.4 82.4 L185.7 84.3 L187.0 86.3 L188.3 88.3 L189.6 90.3 L190.9 92.4 L192.2 94.4 L193.6 96.6 L194.9 98.7 L196.2 100.8 L197.5 103.0 L198.8 105.2 L200.1 107.4 L201.4 109.6 L202.8 111.8 L204.1 114.1 L205.4 116.3 L206.7 118.5 L208.0 120.8 L209.3 123.0 L210.6 125.2 L211.9 127.5 L213.2 129.7 L214.6 131.9 L215.9 134.1 L217.2 136.3 L218.5 138.5 L219.8 140.6 L221.1 142.8 L222.4 144.9 L223.8 147.0 L225.1 149.1 L226.4 151.1 L227.7 153.2 L229.0 155.2 L230.3 157.2 L231.6 159.1 L232.9 161.1 L234.2 163.0 L235.6 164.8 L236.9 166.7 L238.2 168.5 L239.5 170.3 L240.8 172.1 L242.1 173.8 L243.4 175.5 L244.7 177.1 L246.1 178.8 L247.4 180.4 L248.7 181.9 L250.0 183.5 L251.3 185.0 L252.6 186.4 L253.9 187.9 L255.2 189.3 L256.6 190.7 L257.9 192.0 L259.2 193.3 L260.5 194.6 L261.8 195.8 L263.1 197.0 L264.4 198.2 L265.8 199.3 L267.1 200.5 L268.4 201.5 L269.7 202.6 L271.0 203.6 L272.3 204.6 L273.6 205.6 L274.9 206.5 L276.2 207.4 L277.6 208.3 L278.9 209.2 L280.2 210.0 L281.5 210.8 L282.8 211.6 L284.1 212.3 L285.4 213.0 L286.8 213.7 L288.1 214.4 L289.4 215.1 L290.7 215.7 L292.0 216.3 L293.3 216.9 L294.6 217.5 L295.9 218.0 L297.2 218.5 L298.6 219.0 L299.9 219.5 L301.2 220.0 L302.5 220.5 L303.8 220.9 L305.1 221.3 L306.4 221.7 L307.8 222.1 L309.1 222.5 L310.4 222.8 L311.7 223.2 L313.0 223.5 L314.3 223.8 L315.6 224.1 L316.9 224.4 L318.2 224.7 L319.6 224.9 L320.9 225.2 L322.2 225.4 L323.5 225.6 L324.8 225.9 L326.1 226.1 L327.4 226.3 L328.8 226.5 L330.1 226.7 L331.4 226.8 L332.7 227.0 L334.0 227.1 L335.3 227.3 L336.6 227.4 L337.9 227.6 L339.2 227.7 L340.6 227.8 L341.9 228.0 L343.2 228.1 L344.5 228.2 L345.8 228.3 L347.1 228.4 L348.4 228.5 L349.8 228.5 L351.1 228.6 L352.4 228.7 L353.7 228.8 L355.0 228.9 L356.3 228.9 L357.6 229.0 L358.9 229.0 L360.2 229.1 L361.6 229.1 L362.9 229.2 L364.2 229.2 L365.5 229.3 L366.8 229.3 L368.1 229.4 L369.4 229.4 L370.7 229.4 L372.1 229.5 L373.4 229.5 L374.7 229.5 L376.0 229.6 L377.3 229.6 L378.6 229.6 L379.9 229.6 L381.2 229.7 L382.6 229.7 L383.9 229.7 L385.2 229.7 L386.5 229.7 L387.8 229.8 L389.1 229.8 L390.4 229.8 L391.8 229.8 L393.1 229.8 L394.4 229.8 L395.7 229.8 L397.0 229.9 L398.3 229.9 L399.6 229.9 L400.9 229.9 L402.2 229.9 L403.6 229.9 L404.9 229.9 L406.2 229.9 L407.5 229.9 L408.8 229.9 L410.1 229.9 L411.4 229.9 L412.8 229.9 L414.1 229.9 L415.4 229.9 L416.7 230.0 L418.0 230.0 L419.3 230.0 L420.6 230.0 L421.9 230.0 L423.2 230.0 L424.6 230.0 L425.9 230.0 L427.2 230.0 L428.5 230.0 L429.8 230.0 L431.1 230.0 L432.4 230.0 L433.8 230.0 L435.1 230.0 L436.4 230.0 L437.7 230.0 L439.0 230.0 L440.3 230.0 L441.6 230.0 L442.9 230.0 L444.2 230.0 L445.6 230.0 L446.9 230.0 L448.2 230.0 L449.5 230.0 L450.8 230.0 L452.1 230.0 L453.4 230.0 L454.8 230.0 L456.1 230.0 L457.4 230.0 L458.7 230.0 L460.0 230.0" style="fill:none;stroke:var(--indigo);stroke-width:2.2"/><path d="M40.0 230.0 L41.3 230.0 L42.6 229.9 L43.9 229.8 L45.2 229.6 L46.6 229.4 L47.9 229.1 L49.2 228.8 L50.5 228.5 L51.8 228.1 L53.1 227.6 L54.4 227.2 L55.8 226.6 L57.1 226.0 L58.4 225.4 L59.7 224.7 L61.0 224.0 L62.3 223.3 L63.6 222.5 L64.9 221.6 L66.2 220.8 L67.6 219.8 L68.9 218.9 L70.2 217.9 L71.5 216.9 L72.8 215.8 L74.1 214.7 L75.4 213.6 L76.8 212.4 L78.1 211.2 L79.4 209.9 L80.7 208.7 L82.0 207.4 L83.3 206.0 L84.6 204.7 L85.9 203.3 L87.2 201.9 L88.6 200.5 L89.9 199.0 L91.2 197.5 L92.5 196.0 L93.8 194.5 L95.1 193.0 L96.4 191.4 L97.8 189.9 L99.1 188.3 L100.4 186.7 L101.7 185.1 L103.0 183.5 L104.3 181.9 L105.6 180.2 L106.9 178.6 L108.2 176.9 L109.6 175.3 L110.9 173.6 L112.2 171.9 L113.5 170.3 L114.8 168.6 L116.1 167.0 L117.4 165.3 L118.8 163.7 L120.1 162.0 L121.4 160.4 L122.7 158.7 L124.0 157.1 L125.3 155.5 L126.6 153.9 L127.9 152.3 L129.2 150.7 L130.6 149.2 L131.9 147.6 L133.2 146.1 L134.5 144.6 L135.8 143.1 L137.1 141.6 L138.4 140.1 L139.8 138.7 L141.1 137.3 L142.4 135.9 L143.7 134.5 L145.0 133.2 L146.3 131.9 L147.6 130.6 L148.9 129.3 L150.2 128.1 L151.6 126.9 L152.9 125.7 L154.2 124.6 L155.5 123.4 L156.8 122.4 L158.1 121.3 L159.4 120.3 L160.8 119.3 L162.1 118.4 L163.4 117.4 L164.7 116.5 L166.0 115.7 L167.3 114.9 L168.6 114.1 L169.9 113.4 L171.2 112.6 L172.6 112.0 L173.9 111.3 L175.2 110.7 L176.5 110.2 L177.8 109.6 L179.1 109.1 L180.4 108.7 L181.8 108.3 L183.1 107.9 L184.4 107.5 L185.7 107.2 L187.0 107.0 L188.3 106.7 L189.6 106.5 L190.9 106.4 L192.2 106.2 L193.6 106.1 L194.9 106.1 L196.2 106.1 L197.5 106.1 L198.8 106.1 L200.1 106.2 L201.4 106.3 L202.8 106.5 L204.1 106.7 L205.4 106.9 L206.7 107.1 L208.0 107.4 L209.3 107.7 L210.6 108.1 L211.9 108.4 L213.2 108.9 L214.6 109.3 L215.9 109.7 L217.2 110.2 L218.5 110.8 L219.8 111.3 L221.1 111.9 L222.4 112.5 L223.8 113.1 L225.1 113.8 L226.4 114.4 L227.7 115.1 L229.0 115.8 L230.3 116.6 L231.6 117.4 L232.9 118.1 L234.2 119.0 L235.6 119.8 L236.9 120.6 L238.2 121.5 L239.5 122.4 L240.8 123.3 L242.1 124.2 L243.4 125.1 L244.7 126.1 L246.1 127.0 L247.4 128.0 L248.7 129.0 L250.0 130.0 L251.3 131.0 L252.6 132.0 L253.9 133.1 L255.2 134.1 L256.6 135.2 L257.9 136.2 L259.2 137.3 L260.5 138.4 L261.8 139.4 L263.1 140.5 L264.4 141.6 L265.8 142.7 L267.1 143.8 L268.4 144.9 L269.7 146.0 L271.0 147.2 L272.3 148.3 L273.6 149.4 L274.9 150.5 L276.2 151.6 L277.6 152.8 L278.9 153.9 L280.2 155.0 L281.5 156.1 L282.8 157.2 L284.1 158.3 L285.4 159.4 L286.8 160.5 L288.1 161.6 L289.4 162.7 L290.7 163.8 L292.0 164.9 L293.3 166.0 L294.6 167.1 L295.9 168.1 L297.2 169.2 L298.6 170.3 L299.9 171.3 L301.2 172.4 L302.5 173.4 L303.8 174.4 L305.1 175.4 L306.4 176.4 L307.8 177.4 L309.1 178.4 L310.4 179.4 L311.7 180.4 L313.0 181.4 L314.3 182.3 L315.6 183.3 L316.9 184.2 L318.2 185.1 L319.6 186.0 L320.9 186.9 L322.2 187.8 L323.5 188.7 L324.8 189.6 L326.1 190.4 L327.4 191.3 L328.8 192.1 L330.1 192.9 L331.4 193.8 L332.7 194.6 L334.0 195.3 L335.3 196.1 L336.6 196.9 L337.9 197.6 L339.2 198.4 L340.6 199.1 L341.9 199.8 L343.2 200.6 L344.5 201.3 L345.8 201.9 L347.1 202.6 L348.4 203.3 L349.8 203.9 L351.1 204.6 L352.4 205.2 L353.7 205.8 L355.0 206.4 L356.3 207.0 L357.6 207.6 L358.9 208.2 L360.2 208.7 L361.6 209.3 L362.9 209.8 L364.2 210.4 L365.5 210.9 L366.8 211.4 L368.1 211.9 L369.4 212.4 L370.7 212.9 L372.1 213.3 L373.4 213.8 L374.7 214.2 L376.0 214.7 L377.3 215.1 L378.6 215.5 L379.9 215.9 L381.2 216.3 L382.6 216.7 L383.9 217.1 L385.2 217.5 L386.5 217.8 L387.8 218.2 L389.1 218.5 L390.4 218.9 L391.8 219.2 L393.1 219.5 L394.4 219.9 L395.7 220.2 L397.0 220.5 L398.3 220.8 L399.6 221.0 L400.9 221.3 L402.2 221.6 L403.6 221.9 L404.9 222.1 L406.2 222.4 L407.5 222.6 L408.8 222.8 L410.1 223.1 L411.4 223.3 L412.8 223.5 L414.1 223.7 L415.4 223.9 L416.7 224.1 L418.0 224.3 L419.3 224.5 L420.6 224.7 L421.9 224.9 L423.2 225.0 L424.6 225.2 L425.9 225.4 L427.2 225.5 L428.5 225.7 L429.8 225.8 L431.1 226.0 L432.4 226.1 L433.8 226.2 L435.1 226.4 L436.4 226.5 L437.7 226.6 L439.0 226.8 L440.3 226.9 L441.6 227.0 L442.9 227.1 L444.2 227.2 L445.6 227.3 L446.9 227.4 L448.2 227.5 L449.5 227.6 L450.8 227.7 L452.1 227.8 L453.4 227.8 L454.8 227.9 L456.1 228.0 L457.4 228.1 L458.7 228.1 L460.0 228.2" style="fill:none;stroke:var(--coral);stroke-width:2.2"/><line x1="150.5" y1="234.0" x2="150.5" y2="54.7" style="stroke:var(--teal);stroke-width:1.5;stroke-dasharray:4 3"/><text x="147.5" y="245.0" font-size="12" text-anchor="end" style="fill:var(--teal)">v<tspan font-size="9" dy="3">mp</tspan></text><line x1="164.7" y1="251.0" x2="164.7" y2="60.2" style="stroke:var(--amber);stroke-width:1.5;stroke-dasharray:4 3"/><text x="164.7" y="262.0" font-size="12" text-anchor="middle" style="fill:var(--amber)">v<tspan font-size="9" dy="3">avg</tspan></text><line x1="175.4" y1="234.0" x2="175.4" y2="70.5" style="stroke:var(--plum);stroke-width:1.5;stroke-dasharray:4 3"/><text x="178.4" y="245.0" font-size="12" text-anchor="start" style="fill:var(--plum)">v<tspan font-size="9" dy="3">rms</tspan></text><text x="108.5" y="101.3" font-size="12" text-anchor="end" style="fill:var(--indigo)">T₁</text><text x="294.2" y="158.7" font-size="12" style="fill:var(--coral)">T₂ = 2T₁</text><text x="34" y="245" font-size="12" style="fill:var(--muted)">0</text><text x="460" y="50" font-size="12" text-anchor="end" style="fill:var(--muted)">Hotter gas: peak moves right and drops.</text><text x="460" y="66" font-size="12" text-anchor="end" style="fill:var(--muted)">Area under each curve is the same.</text></svg>')

FIG_CUBE = ('<svg viewBox="0 0 480 250" role="img" aria-label="Molecule bouncing between opposite walls of a cube of side L, with momentum before and after hitting the right wall"><rect x="60" y="60" width="150" height="150" style="fill:var(--water-soft);stroke:var(--ink-2);stroke-width:1.5"/><path d="M60 60 L100 30 L250 30 L210 60 M250 30 L250 180 L210 210" style="fill:none;stroke:var(--ink-2);stroke-width:1.5"/><path d="M210 60 L250 30 L250 180 L210 210 Z" style="fill:var(--coral-soft);stroke:var(--coral);stroke-width:1.5"/><text x="256" y="153.0" font-size="12" style="fill:var(--coral)">wall A</text><text x="256" y="168.0" font-size="12" style="fill:var(--coral)">(area L²)</text><path d="M95 150 L205 115 L115 75" style="fill:none;stroke:var(--muted);stroke-width:1.2;stroke-dasharray:4 3"/><circle cx="95" cy="150" r="6" style="fill:var(--indigo);stroke:var(--ink-2);stroke-width:1"/><line x1="95" y1="150" x2="150" y2="136" style="stroke:var(--indigo);stroke-width:2"/><path d="M150 136 L140 135 L144 143 Z" style="fill:var(--indigo)"/><text x="105" y="172" font-size="12" style="fill:var(--indigo)">velocity v, x-part vₓ</text><line x1="60" y1="228" x2="210" y2="228" style="stroke:var(--ink-2);stroke-width:1"/><line x1="60" y1="222" x2="60" y2="234" style="stroke:var(--ink-2);stroke-width:1"/><line x1="210" y1="222" x2="210" y2="234" style="stroke:var(--ink-2);stroke-width:1"/><text x="131.0" y="246" font-size="12" style="fill:var(--ink)">L</text><text x="218" y="230" font-size="12" style="fill:var(--ink)">x</text><text x="300" y="28" font-size="12" style="fill:var(--ink)">At wall A (x-direction only):</text><text x="300" y="46" font-size="12" style="fill:var(--ink-2)">before: +m vₓ</text><text x="300" y="64" font-size="12" style="fill:var(--ink-2)">after: −m vₓ</text><text x="300" y="82" font-size="12" style="fill:var(--coral)">impulse on wall: 2m vₓ</text><text x="300" y="100" font-size="12" style="fill:var(--ink-2)">time between hits on A: 2L/vₓ</text><text x="300" y="118" font-size="12" style="fill:var(--indigo)">average force: m vₓ²/L</text></svg>')

FIG_ISOCHORES = ('<svg viewBox="0 0 420 250" role="img" aria-label="Pressure against absolute temperature for a fixed amount of gas at three constant volumes; straight lines through the origin, steepest for the smallest volume"><line x1="55" y1="215" x2="370" y2="215" style="stroke:var(--ink-2);stroke-width:1.5"/><line x1="55" y1="215" x2="55" y2="25" style="stroke:var(--ink-2);stroke-width:1.5"/><text x="330" y="235" font-size="12" style="fill:var(--ink)">T (K)</text><text x="25" y="35" font-size="12" style="fill:var(--ink)">P</text><text x="41" y="231" font-size="12" style="fill:var(--muted)">O</text><line x1="55" y1="215" x2="153.1" y2="45.0" style="stroke:var(--coral);stroke-width:2"/><text x="159.1" y="49.0" font-size="12" style="fill:var(--coral)">V₁ (smallest)</text><line x1="55" y1="215" x2="257.6" y2="45.0" style="stroke:var(--indigo);stroke-width:2"/><text x="263.6" y="49.0" font-size="12" style="fill:var(--indigo)">V₂</text><line x1="55" y1="215" x2="333.2" y2="102.6" style="stroke:var(--teal);stroke-width:2"/><text x="339.2" y="106.6" font-size="12" style="fill:var(--teal)">V₃ (largest)</text><line x1="135" y1="215" x2="135" y2="76.4" style="stroke:var(--muted);stroke-width:1;stroke-dasharray:4 3"/><text x="129" y="231" font-size="12" style="fill:var(--muted)">T₀</text><text x="220" y="173" font-size="12" style="fill:var(--muted)">At the same T₀ the steepest</text><text x="220" y="188" font-size="12" style="fill:var(--muted)">line has the highest P.</text><text x="220" y="206" font-size="12" style="fill:var(--ink-2)">slope = nR/V</text></svg>')

FIG_CYLINDER = ('<svg viewBox="0 0 460 245" role="img" aria-label="Collision cylinder of radius d swept by a moving molecule; molecules whose centres lie inside the cylinder are hit"><rect x="70" y="72" width="310" height="80" style="fill:var(--amber-soft);stroke:none"/><line x1="70" y1="72" x2="380" y2="72" style="stroke:var(--amber);stroke-width:1.5"/><line x1="70" y1="152" x2="380" y2="152" style="stroke:var(--amber);stroke-width:1.5"/><ellipse cx="70" cy="112" rx="12" ry="40" style="fill:var(--amber-soft);stroke:var(--amber);stroke-width:1.5"/><ellipse cx="380" cy="112" rx="12" ry="40" style="fill:none;stroke:var(--amber);stroke-width:1.5;stroke-dasharray:4 3"/><line x1="70" y1="112" x2="420" y2="112" style="stroke:var(--muted);stroke-width:1;stroke-dasharray:3 3"/><circle cx="70" cy="112" r="20" style="fill:var(--indigo);stroke:var(--ink-2);stroke-width:1"/><path d="M420 112 L410 107 L410 117 Z" style="fill:var(--muted)"/><line x1="110" y1="112" x2="110" y2="72" style="stroke:var(--ink);stroke-width:1.2"/><text x="115" y="96.0" font-size="12" style="fill:var(--ink)">d</text><circle cx="170" cy="137" r="20" style="fill:none;stroke:var(--coral);stroke-width:1.5"/><circle cx="170" cy="137" r="2.5" style="fill:var(--coral)"/><circle cx="240" cy="82" r="20" style="fill:none;stroke:var(--coral);stroke-width:1.5"/><circle cx="240" cy="82" r="2.5" style="fill:var(--coral)"/><circle cx="310" cy="120" r="20" style="fill:none;stroke:var(--coral);stroke-width:1.5"/><circle cx="310" cy="120" r="2.5" style="fill:var(--coral)"/><circle cx="200" cy="52" r="20" style="fill:none;stroke:var(--teal);stroke-width:1.5"/><circle cx="200" cy="52" r="2.5" style="fill:var(--teal)"/><circle cx="240" cy="178" r="20" style="fill:none;stroke:var(--teal);stroke-width:1.5"/><circle cx="240" cy="178" r="2.5" style="fill:var(--teal)"/><circle cx="350" cy="54" r="20" style="fill:none;stroke:var(--teal);stroke-width:1.5"/><circle cx="350" cy="54" r="2.5" style="fill:var(--teal)"/><line x1="70" y1="202" x2="380" y2="202" style="stroke:var(--ink-2);stroke-width:1"/><text x="165.0" y="219" font-size="12" style="fill:var(--ink)">length swept = v̄ t</text><text x="30" y="20" font-size="12" style="fill:var(--coral)">centre inside the cylinder: collision</text><text x="260" y="20" font-size="12" style="fill:var(--teal)">centre outside: missed</text><text x="20" y="180" font-size="12" style="fill:var(--indigo)">moving molecule, diameter d</text></svg>')

FIG_CV_H2 = ('<svg viewBox="0 0 440 250" role="img" aria-label="Qualitative molar heat capacity at constant volume of hydrogen gas against temperature on a log scale, rising in steps from 3R/2 to 5R/2 to 7R/2"><line x1="70" y1="205" x2="420" y2="205" style="stroke:var(--ink-2);stroke-width:1.5"/><line x1="70" y1="205" x2="70" y2="20" style="stroke:var(--ink-2);stroke-width:1.5"/><line x1="70" y1="175.8" x2="400" y2="175.8" style="stroke:var(--line-2);stroke-width:1;stroke-dasharray:3 4"/><text x="30" y="179.8" font-size="12" style="fill:var(--ink-2)">3R/2</text><line x1="70" y1="117.5" x2="400" y2="117.5" style="stroke:var(--line-2);stroke-width:1;stroke-dasharray:3 4"/><text x="30" y="121.5" font-size="12" style="fill:var(--ink-2)">5R/2</text><line x1="70" y1="59.2" x2="400" y2="59.2" style="stroke:var(--line-2);stroke-width:1;stroke-dasharray:3 4"/><text x="30" y="63.2" font-size="12" style="fill:var(--ink-2)">7R/2</text><path d="M70.0 175.7 L71.7 175.7 L73.3 175.7 L75.0 175.7 L76.6 175.7 L78.2 175.7 L79.9 175.6 L81.6 175.6 L83.2 175.6 L84.8 175.6 L86.5 175.5 L88.1 175.5 L89.8 175.4 L91.5 175.4 L93.1 175.3 L94.8 175.3 L96.4 175.2 L98.0 175.1 L99.7 175.0 L101.3 174.9 L103.0 174.8 L104.6 174.7 L106.3 174.5 L108.0 174.4 L109.6 174.2 L111.2 174.0 L112.9 173.8 L114.5 173.5 L116.2 173.2 L117.9 172.9 L119.5 172.6 L121.2 172.2 L122.8 171.7 L124.5 171.2 L126.1 170.7 L127.8 170.1 L129.4 169.4 L131.1 168.7 L132.7 167.9 L134.4 167.1 L136.0 166.1 L137.7 165.1 L139.3 164.0 L140.9 162.8 L142.6 161.6 L144.2 160.2 L145.9 158.8 L147.6 157.3 L149.2 155.7 L150.8 154.1 L152.5 152.4 L154.2 150.7 L155.8 149.0 L157.4 147.2 L159.1 145.5 L160.8 143.7 L162.4 142.0 L164.1 140.3 L165.7 138.6 L167.3 137.0 L169.0 135.5 L170.6 134.0 L172.3 132.6 L173.9 131.3 L175.6 130.1 L177.3 128.9 L178.9 127.8 L180.5 126.9 L182.2 125.9 L183.9 125.1 L185.5 124.3 L187.1 123.6 L188.8 123.0 L190.4 122.4 L192.1 121.9 L193.8 121.4 L195.4 121.0 L197.1 120.6 L198.7 120.3 L200.4 120.0 L202.0 119.7 L203.6 119.5 L205.3 119.3 L206.9 119.1 L208.6 118.9 L210.2 118.7 L211.9 118.6 L213.6 118.5 L215.2 118.4 L216.9 118.3 L218.5 118.2 L220.1 118.1 L221.8 118.0 L223.5 118.0 L225.1 117.9 L226.7 117.8 L228.4 117.8 L230.1 117.8 L231.7 117.7 L233.3 117.7 L235.0 117.7 L236.7 117.6 L238.3 117.6 L239.9 117.6 L241.6 117.6 L243.3 117.5 L244.9 117.5 L246.5 117.5 L248.2 117.5 L249.9 117.4 L251.5 117.4 L253.1 117.4 L254.8 117.4 L256.5 117.3 L258.1 117.3 L259.8 117.3 L261.4 117.2 L263.1 117.2 L264.7 117.2 L266.3 117.1 L268.0 117.1 L269.7 117.0 L271.3 117.0 L272.9 116.9 L274.6 116.8 L276.2 116.7 L277.9 116.6 L279.6 116.5 L281.2 116.4 L282.9 116.3 L284.5 116.2 L286.1 116.0 L287.8 115.8 L289.5 115.6 L291.1 115.4 L292.8 115.2 L294.4 114.9 L296.0 114.6 L297.7 114.3 L299.3 114.0 L301.0 113.6 L302.7 113.1 L304.3 112.7 L305.9 112.2 L307.6 111.6 L309.2 111.0 L310.9 110.3 L312.5 109.6 L314.2 108.8 L315.9 107.9 L317.5 107.0 L319.1 106.0 L320.8 104.9 L322.5 103.8 L324.1 102.6 L325.8 101.3 L327.4 99.9 L329.1 98.5 L330.7 97.1 L332.3 95.6 L334.0 94.0 L335.7 92.4 L337.3 90.8 L339.0 89.2 L340.6 87.6 L342.2 86.0 L343.9 84.4 L345.6 82.8 L347.2 81.2 L348.8 79.7 L350.5 78.3 L352.1 76.8 L353.8 75.5 L355.5 74.2 L357.1 73.0 L358.8 71.9 L360.4 70.8 L362.1 69.8 L363.7 68.9 L365.3 68.0 L367.0 67.2 L368.7 66.4 L370.3 65.8 L371.9 65.1 L373.6 64.6 L375.2 64.0 L376.9 63.6 L378.5 63.1 L380.2 62.7 L381.9 62.4 L383.5 62.1 L385.1 61.8 L386.8 61.5 L388.4 61.3 L390.1 61.0 L391.7 60.9 L393.4 60.7 L395.0 60.5 L396.7 60.4 L398.4 60.3 L400.0 60.1" style="fill:none;stroke:var(--indigo);stroke-width:2.2"/><line x1="163.7" y1="205" x2="163.7" y2="210" style="stroke:var(--ink-2);stroke-width:1"/><text x="145.7" y="224" font-size="12" style="fill:var(--ink-2)">100 K</text><line x1="277.3" y1="205" x2="277.3" y2="210" style="stroke:var(--ink-2);stroke-width:1"/><text x="259.3" y="224" font-size="12" style="fill:var(--ink-2)">1000 K</text><line x1="217.9" y1="205" x2="217.9" y2="117.5" style="stroke:var(--amber);stroke-width:1;stroke-dasharray:4 3"/><text x="209.9" y="238" font-size="12" style="fill:var(--amber)">room temperature</text><text x="345" y="224" font-size="12" style="fill:var(--ink)">T (log)</text><text x="74" y="18" font-size="12" style="fill:var(--ink)">C<tspan font-size="9" dy="3">V</tspan></text><text x="79.0" y="192.8" font-size="12" style="fill:var(--teal)">translation only</text><text x="210.8" y="109.5" font-size="12" style="fill:var(--teal)">+ rotation</text><text x="297.3" y="51.2" font-size="12" style="fill:var(--teal)">+ vibration</text></svg>')


DEEP = {
# ---------------------------------------------------------------- gas law
'kinetic-theory-gas-law': dict(
    level='basic',
    notes=[
        ('Assumptions of the kinetic theory', r'''<p>Open a bottle of perfume in one corner of a room and you smell it in the far corner a little later. Gas molecules are always moving, and they spread out to fill whatever space they get. Kinetic theory turns that picture into numbers. It works because it makes a few simple assumptions about the molecules:</p>
<ol>
<li>A gas is made of a very large number of identical molecules. Each one behaves like a tiny hard sphere.</li>
<li>The molecules themselves take up negligible volume compared with the container.</li>
<li>They move randomly in all directions and obey Newton’s laws.</li>
<li>There are no forces between molecules except during collisions, so they move in straight lines between collisions. Gravity on them is neglected.</li>
<li>Collisions with each other and with the walls are perfectly elastic, so kinetic energy is conserved.</li>
<li>A collision lasts a negligible time compared with the time between collisions.</li>
</ol>
<p>A gas that obeys these assumptions exactly is an <strong>ideal gas</strong>. Real gases come close at low pressure and high temperature, where molecules are far apart and fast.</p>'''),
        ('The gas laws are special cases of PV = nRT', r'''<p>Hold two of the four quantities (n, P, V, T) fixed and the equation of state gives one of the named laws.</p>
<ul>
<li><strong>Boyle’s law</strong> (n, T fixed): \(PV=\) constant. The P–V graph is a rectangular hyperbola. A hotter isotherm lies farther from the origin. A graph of PV against P is a horizontal line at height nRT.</li>
<li><strong>Charles’s law</strong> (n, P fixed): \(V\propto T\). The V–T graph is a straight line through the origin, with slope nR/P. A steeper line means a <em>lower</em> pressure.</li>
<li><strong>Gay-Lussac’s (pressure) law</strong> (n, V fixed): \(P\propto T\). The P–T graph is a straight line through the origin, with slope nR/V. A steeper line means a <em>smaller</em> volume.</li>
<li><strong>Avogadro’s law</strong> (P, T fixed): \(V\propto n\). Equal volumes of all ideal gases at the same P and T hold the same number of molecules. One mole occupies about 22.4 L at 0 °C and 1 atm.</li>
</ul>
<p>If T is plotted in °C instead of K, the V–T and P–T lines no longer pass through the origin. Extended backwards, they all meet the temperature axis at −273.15 °C.</p>
<p>To compare two states on any graph, draw lines from the origin. On a P–T graph, the state on the steeper line from O has the smaller volume, because \(V=nR\,(T/P)\).</p>'''),
        ('Useful rearrangements and real gases', r'''<p>Write \(n=m/M\) to bring in mass and density: \(P=\dfrac{\rho RT}{M}\). At fixed P and T, gas density is proportional to molar mass. Write \(N=PV/(k_BT)\) to count molecules: the number density is \(P/(k_BT)\), the same for every ideal gas at the same P and T.</p>
<p>Real gases depart from PV = nRT at high pressure and low temperature. Molecules then occupy a noticeable part of the volume and attract each other. The van der Waals equation \(\left(P+\dfrac{an^2}{V^2}\right)(V-nb)=nRT\) corrects for both effects: <em>b</em> for molecular volume and <em>a</em> for attraction. For NEET you only need the idea: a real gas behaves most ideally at low pressure and high temperature.</p>'''),
    ],
    formulas=[
        dict(title='Density form of the gas equation', formula=r'P=\frac{\rho RT}{M}\quad\Rightarrow\quad \rho=\frac{PM}{RT}',
             symbols='P absolute pressure (Pa); ρ gas density (kg/m³); R = 8.31 J/mol K; T absolute temperature (K); M molar mass in kg/mol, not g/mol. Ideal gas.'),
        dict(title='Number density', formula=r'n_N=\frac{N}{V}=\frac{P}{k_BT}',
             symbols='n_N molecules per unit volume (m⁻³); N number of molecules; V volume (m³); P pressure (Pa); k_B = 1.38×10⁻²³ J/K; T absolute temperature (K). Same for all ideal gases at given P and T.'),
    ],
    figure=dict(svg=FIG_ISOCHORES,
                caption='P–T graph for a fixed amount of ideal gas held at three different constant volumes. Each isochore is a straight line through the origin with slope nR/V, so the steepest line belongs to the smallest volume.'),
    traps=[
        r'Proportionality uses kelvin. Heating a gas from 27 °C to 54 °C at constant volume does not double its pressure. The ratio is 327/300 = 1.09.',
        r'On a P–T or V–T graph, a steeper line through the origin means a <em>smaller</em> volume (P–T) or a <em>smaller</em> pressure (V–T). Students often read steeper as larger.',
    ],
    exam=r'''<ul>
<li>“Two isochores (or isobars) make angles θ₁ and θ₂ with the T axis. Find V₁/V₂ (or P₁/P₂).” Use slope = tan θ ∝ 1/V or 1/P.</li>
<li>“A gas leaks from a cylinder and both P and T fall. What fraction of gas escaped?” Use m ∝ PV/T at fixed V.</li>
<li>“An air bubble rises from the bottom of a lake and its volume becomes k times. Find the depth.”</li>
<li>Graph shape questions: PV against P at constant T, P against 1/V, V against T in °C.</li>
<li>Density of a gas at given P and T, or comparing densities of two gases (ρ ∝ PM/T).</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'Find the density of oxygen gas (M = 32 g/mol) at 27 °C and 1.013×10⁵ Pa. Take R = 8.31 J/mol K.',
             steps=[r'Convert units: M = 0.032 kg/mol and T = 27 + 273 = 300 K.',
                    r'Use \(\rho=PM/(RT)\).',
                    r'\(\rho=\dfrac{1.013\times10^5\times0.032}{8.31\times300}=\dfrac{3241.6}{2493}\approx1.30\) kg/m³.',
                    r'Check: air (M ≈ 29 g/mol) has density about 1.2 kg/m³ at room conditions, so a slightly heavier gas at about 1.3 kg/m³ is sensible.'],
             answer=r'About 1.30 kg/m³.'),
        dict(tag='Numerical', q=r'An air bubble rises from the bottom of a lake to the surface and its volume becomes three times larger. Temperature stays constant. Atmospheric pressure is 10⁵ Pa, water density is 1000 kg/m³ and g = 10 m/s². How deep is the lake?',
             steps=[r'Temperature and the amount of air are fixed, so Boyle’s law applies: \(P_1V_1=P_2V_2\).',
                    r'At the surface P₂ = P₀ and V₂ = 3V₁. So the pressure at the bottom is \(P_1=3P_0\).',
                    r'At depth h, \(P_1=P_0+\rho gh\). So \(\rho gh=2P_0\).',
                    r'\(h=\dfrac{2\times10^5}{1000\times10}=20\) m.'],
             answer=r'20 m.'),
        dict(tag='Graph', q=r'A fixed mass of ideal gas goes from state A (300 K, 1.0 atm) to state B (600 K, 1.5 atm). On a P–T graph, which state lies on the steeper line drawn from the origin, and does the volume increase or decrease?',
             steps=[r'For each state, the line from the origin has slope \(P/T=nR/V\).',
                    r'Slope at A = 1.0/300 = 1/300. Slope at B = 1.5/600 = 1/400.',
                    r'A lies on the steeper line, so A has the smaller volume.',
                    r'Check directly: \(V\propto T/P\). \(V_B/V_A=(600/1.5)/(300/1.0)=400/300=4/3\).'],
             answer=r'A is on the steeper line. The volume increases by a factor 4/3 from A to B.'),
    ],
    practice=[
        dict(type='graph', q=r'Two isobars for the same amount of an ideal gas are drawn on a V–T graph (T in kelvin). Isobar 1 makes 60° with the T axis and isobar 2 makes 30°. The pressures P₁ and P₂ satisfy',
             options=['P₁ = 3P₂', 'P₁ = P₂', 'P₂ = 3P₁', 'P₂ = √3 P₁'], answer=2,
             explanation=r'On a V–T graph the slope is nR/P, so P ∝ 1/tan θ. P₂/P₁ = tan 60°/tan 30° = √3/(1/√3) = 3. P₁ = 3P₂ wrongly takes the steeper line as the higher pressure. √3 uses only one of the two tangents.'),
        dict(type='numerical', q=r'A rigid cylinder holds gas at 15 atm and 27 °C. Some gas leaks out, and the pressure falls to 10 atm while the temperature falls to 17 °C. What fraction of the original gas escaped?',
             options=['1/3', '9/29', '20/29', '1/2'], answer=1,
             explanation=r'At fixed V, the amount n ∝ P/T. n₂/n₁ = (10/290)/(15/300) = 20/29, so the fraction lost is 1 − 20/29 = 9/29 ≈ 0.31. 1/3 ignores the drop in temperature. 20/29 is the fraction that remains, not the fraction lost.'),
        dict(type='statement', q=r'Statement I: Equal volumes of all ideal gases at the same temperature and pressure contain equal numbers of molecules. Statement II: At 0 °C and 1 atm, one mole of any ideal gas occupies about 22.4 L.',
             options=['Both statements are correct', 'Both statements are incorrect', 'Statement I is correct but Statement II is incorrect', 'Statement I is incorrect but Statement II is correct'], answer=0,
             explanation=r'N = PV/(k_BT) contains no property of the gas, so Statement I (Avogadro’s law) is correct. V = nRT/P = 1×8.31×273/(1.013×10⁵) ≈ 0.0224 m³ = 22.4 L, so Statement II is also correct. Neither statement depends on molar mass.'),
        dict(type='concept', q=r'For a fixed amount of ideal gas at constant temperature, a graph of PV (y-axis) against P (x-axis) is',
             options=['A straight line through the origin with positive slope', 'A rectangular hyperbola', 'A straight line with negative slope', 'A straight line parallel to the P axis'], answer=3,
             explanation=r'PV = nRT is the same at every pressure when n and T are fixed, so the graph is a horizontal line. The rectangular hyperbola is the P–V graph, not the PV–P graph. Real gases show curves on this plot, which is why it tests ideal behaviour.'),
    ],
),
# ---------------------------------------------------------------- pressure
'kinetic-theory-pressure': dict(
    notes=[
        ('Derivation: pressure from molecular collisions', r'''<p>Take a cube of side L containing N molecules, each of mass m. Look at one molecule with velocity components \((v_x, v_y, v_z)\) and follow its motion along x.</p>
<ol>
<li>It hits the right wall (wall A, area L²) and bounces back elastically. Its x-momentum changes from \(+mv_x\) to \(-mv_x\). The change is \(-2mv_x\), so the wall receives an impulse \(2mv_x\). The y and z components do not change.</li>
<li>Before it hits wall A again it must cross to the far wall and come back, a distance 2L. Time between hits on wall A: \(\Delta t=2L/v_x\).</li>
<li>Average force on wall A from this molecule: \(\dfrac{2mv_x}{2L/v_x}=\dfrac{mv_x^2}{L}\).</li>
<li>Add all N molecules: \(F=\dfrac{m}{L}\sum v_x^2=\dfrac{mN}{L}\langle v_x^2\rangle\).</li>
<li>Pressure: \(P=\dfrac{F}{L^2}=\dfrac{mN}{V}\langle v_x^2\rangle\).</li>
<li>Motion is random, so no direction is special: \(\langle v_x^2\rangle=\langle v_y^2\rangle=\langle v_z^2\rangle\). Since \(v^2=v_x^2+v_y^2+v_z^2\), each equals \(\langle v^2\rangle/3\).</li>
<li>Therefore \(P=\dfrac13\dfrac{mN}{V}\langle v^2\rangle=\dfrac13\rho v_{rms}^2\), with \(\rho=mN/V\).</li>
</ol>
<p>Collisions between molecules do not spoil the result. Momentum is conserved in each collision, so on average the momentum delivered to the wall is unchanged. The shape of the container does not matter either; the cube just keeps the algebra simple.</p>'''),
        ('Pressure, kinetic energy and the meaning of temperature', r'''<p>Multiply \(P=\frac13\frac{mN}{V}v_{rms}^2\) by V: \(PV=\frac13Nmv_{rms}^2=\frac23\left(\frac12Nmv_{rms}^2\right)=\frac23E\), where E is the total translational kinetic energy. So <strong>pressure equals two-thirds of the translational kinetic energy per unit volume</strong>.</p>
<p>Now compare with the ideal gas law \(PV=Nk_BT\). Then \(\frac23E=Nk_BT\), so the average translational kinetic energy of one molecule is \(\frac12mv_{rms}^2=\frac32k_BT\).</p>
<p>This is the kinetic meaning of temperature: absolute temperature measures the average translational kinetic energy of the molecules. It does not depend on the mass of the molecule, the pressure or the kind of gas. A hydrogen molecule and an oxygen molecule in the same room have the same average translational kinetic energy.</p>
<p>The “rms” in \(v_{rms}\) means root of the mean of the squares. For speeds 1, 2, 3, 4 and 5 km/s, the mean is 3 km/s but \(v_{rms}=\sqrt{(1+4+9+16+25)/5}=\sqrt{11}\approx3.32\) km/s. Squaring gives more weight to the fast molecules, so \(v_{rms}\) is always at least the mean speed.</p>'''),
    ],
    formulas=[
        dict(title='Pressure from molecular quantities', formula=r'P=\frac13\,\frac{mN}{V}\,v_{rms}^2=\frac13\,m\,n_N\,v_{rms}^2',
             symbols='P pressure (Pa); m mass of one molecule (kg); N number of molecules; V volume (m³); n_N = N/V number density (m⁻³); v_rms root-mean-square speed (m/s). Ideal gas, random isotropic motion, elastic collisions.'),
        dict(title='Pressure and kinetic energy', formula=r'PV=\frac23E,\qquad P=\frac23\,\frac{E}{V},\qquad \frac12mv_{rms}^2=\frac32k_BT',
             symbols='E total translational kinetic energy of the gas (J); E/V translational KE per unit volume (J/m³); k_B = 1.38×10⁻²³ J/K; T absolute temperature (K). Only translational energy enters, even for diatomic gases.'),
    ],
    figure=dict(svg=FIG_CUBE,
                caption='One molecule bouncing inside a cube of side L. Only the x-component of momentum reverses at wall A, so each hit delivers 2mvₓ. The molecule returns to wall A after a round trip of 2L, which takes 2L/vₓ.'),
    traps=[
        r'The factor 1/3 comes from sharing ⟨v²⟩ equally among three directions. It does not come from the cube having three pairs of walls.',
        r'PV = (2/3)E uses only <em>translational</em> kinetic energy. For a diatomic gas the total internal energy is larger, so PV ≠ (2/3)U for O₂ or N₂.',
    ],
    exam=r'''<ul>
<li>“Find the pressure from density and rms speed”, or the reverse, using P = ρv²ᵣₘₛ/3.</li>
<li>“The kinetic energy per unit volume of a gas at pressure P is …” Answer: 3P/2.</li>
<li>Steps of the derivation: impulse per collision (2mvₓ), time between collisions with the same wall (2L/vₓ).</li>
<li>Ratio questions: what happens to P if the mass of each molecule halves and the speed doubles at fixed number density.</li>
<li>Assertion–reason on why pressure is the same on all walls, or why a moving container does not change gas pressure.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A 2.0 L container holds an ideal gas at 1.0×10⁵ Pa. Find the total translational kinetic energy of the molecules.',
             steps=[r'Use \(PV=\frac23E\), so \(E=\frac32PV\).',
                    r'Convert volume: 2.0 L = 2.0×10⁻³ m³.',
                    r'\(E=1.5\times1.0\times10^5\times2.0\times10^{-3}=300\) J.',
                    r'The answer does not depend on the type of gas, because only translational energy is involved.'],
             answer=r'300 J.'),
        dict(tag='Ratio', q=r'In a gas, the mass of each molecule is halved and its rms speed is doubled. The number of molecules per unit volume is unchanged. By what factor does the pressure change?',
             steps=[r'\(P=\frac13mn_Nv_{rms}^2\), so \(P\propto mv_{rms}^2\) at fixed \(n_N\).',
                    r'New factor = \(\frac12\times2^2=2\).',
                    r'The pressure doubles. Each impact delivers less momentum (half the mass, double the speed gives the same momentum per hit) but impacts happen twice as often.'],
             answer=r'The pressure doubles.'),
        dict(tag='Concept', q=r'Five molecules have speeds 1, 2, 3, 4 and 5 km/s. Find their mean speed and rms speed. Which one decides the pressure?',
             steps=[r'Mean speed = (1 + 2 + 3 + 4 + 5)/5 = 3 km/s.',
                    r'Mean of squares = (1 + 4 + 9 + 16 + 25)/5 = 11 (km/s)².',
                    r'\(v_{rms}=\sqrt{11}\approx3.32\) km/s, larger than the mean speed.',
                    r'Pressure depends on momentum transfer per hit (∝ v) times hit rate (∝ v), so it depends on ⟨v²⟩, that is on \(v_{rms}\).'],
             answer=r'Mean speed 3 km/s, rms speed about 3.32 km/s. Pressure depends on the rms speed.'),
    ],
    practice=[
        dict(type='ar', q=r'Assertion (A): Neglecting gravity, an ideal gas in a cubical box exerts the same pressure on all six walls. Reason (R): For random molecular motion, ⟨vₓ²⟩ = ⟨v_y²⟩ = ⟨v_z²⟩ = ⟨v²⟩/3.',
             options=['Both A and R are true and R is the correct explanation of A', 'Both A and R are true but R is not the correct explanation of A', 'A is true but R is false', 'A is false but R is true'], answer=0,
             explanation=r'The pressure on a wall depends on the mean square velocity component perpendicular to it. Isotropy makes all three components equal, so every wall feels the same pressure. R is exactly the reason. Gravity would add a small height dependence, which the assertion excludes.'),
        dict(type='numerical', q=r'An ideal gas is at a pressure of 2.0×10⁵ Pa. The total translational kinetic energy of its molecules per cubic metre is',
             options=['1.33×10⁵ J', '2.0×10⁵ J', '4.0×10⁵ J', '3.0×10⁵ J'], answer=3,
             explanation=r'P = (2/3)(E/V), so E/V = 3P/2 = 3.0×10⁵ J/m³. 1.33×10⁵ J comes from inverting the factor (2P/3). 2.0×10⁵ J simply equates energy density with pressure.'),
        dict(type='concept', q=r'In the kinetic-theory derivation of pressure, a molecule with x-velocity vₓ moves in a cube of side L. The time between two successive collisions of this molecule with the same wall is',
             options=['L/vₓ', '2L/vₓ', 'L/(2vₓ)', '2L/v, where v is the full speed'], answer=1,
             explanation=r'Between two hits on the same wall the molecule crosses to the opposite wall and back, covering 2L in the x-direction at speed vₓ. L/vₓ is only one crossing. Using the full speed v is wrong because only the x-motion carries it between these two walls.'),
        dict(type='multi', q=r'An ideal gas in a rigid sealed container is heated. Which of these statements are correct? (a) Each wall receives more molecular hits per second. (b) The average momentum delivered per hit increases. (c) The mean free path of the molecules increases.',
             options=['(a) only', '(b) only', '(a) and (b) only', '(a), (b) and (c)'], answer=2,
             explanation=r'Faster molecules hit the walls more often and deliver more momentum per hit; both effects scale with v, so P ∝ v²ᵣₘₛ ∝ T. The mean free path 1/(√2πd²n_N) depends on number density, which is fixed in a sealed rigid box, so (c) is wrong.'),
    ],
),
# ---------------------------------------------------------------- speeds
'kinetic-theory-speeds': dict(
    level='exam',
    notes=[
        ('Kinetic energy per molecule and per mole', r'''<p>From the pressure derivation, every ideal-gas molecule has average translational kinetic energy \(\frac32k_BT\), whatever its mass. At 300 K this is \(1.5\times1.38\times10^{-23}\times300\approx6.2\times10^{-21}\) J. One mole contains \(N_A\) molecules, so its translational kinetic energy is \(\frac32RT\).</p>
<p>Since \(\frac12mv_{rms}^2=\frac32k_BT\), we get \(v_{rms}=\sqrt{3k_BT/m}=\sqrt{3RT/M}\). Using \(P=\rho RT/M\) this is also \(v_{rms}=\sqrt{3P/\rho}\).</p>
<ul>
<li>At a fixed temperature, \(v_{rms}\propto1/\sqrt{M}\): lighter gases move faster.</li>
<li>For a given gas, \(v_{rms}\propto\sqrt{T}\). Changing pressure at constant temperature does not change \(v_{rms}\), because density changes in the same ratio as pressure.</li>
<li>Classically, all molecular motion would stop at T = 0 K. That is the kinetic meaning of absolute zero.</li>
</ul>'''),
        ('Three speeds and their fixed ratio', r'''<p>The molecules in a gas do not all move at the same speed. Three summaries of the distribution are used:</p>
<ul>
<li>Most probable speed \(v_{mp}=\sqrt{2RT/M}\): the speed at the peak of the distribution.</li>
<li>Average (mean) speed \(\bar v=\sqrt{8RT/(\pi M)}\): the ordinary average of the speeds.</li>
<li>Rms speed \(v_{rms}=\sqrt{3RT/M}\): the square root of the average of v².</li>
</ul>
<p>All three have the form \(\sqrt{\text{number}\times RT/M}\), so their ratio is fixed for every gas at every temperature:</p>
<p>\[v_{rms}:\bar v:v_{mp}=\sqrt3:\sqrt{8/\pi}:\sqrt2\approx1.73:1.60:1.41\]</p>
<p>So \(v_{rms}>\bar v>v_{mp}\). The mean vector velocity is zero, because molecules move equally in all directions. Never use it in place of a speed.</p>'''),
        ('Maxwell speed distribution, escape of light gases and sound', r'''<p>The Maxwell distribution gives the fraction of molecules per unit speed interval. Its shape:</p>
<ul>
<li>It starts at zero (very few molecules are almost at rest), rises to a peak at \(v_{mp}\), then falls with a long tail of fast molecules.</li>
<li>The area under the curve is the total number (or fraction) of molecules, so it stays the same when T changes.</li>
<li>At higher T the peak moves to a higher speed and becomes lower, and the curve spreads out. The area stays the same.</li>
<li>At the same T, a heavier gas has a narrower, taller curve peaked at a lower speed. Raising M has the same effect as lowering T, because only T/M appears.</li>
</ul>
<p><strong>Why Earth has almost no hydrogen.</strong> Escape speed from Earth is 11.2 km/s. At 300 K, \(v_{rms}\) of H₂ is only about 1.9 km/s. But the long tail always contains some molecules faster than the escape speed, and for light molecules this fraction is much larger. Over millions of years H₂ and He leak away, while N₂ and O₂ stay. The Moon’s escape speed is only about 2.4 km/s, so it has lost almost all its atmosphere.</p>
<p><strong>Sound versus molecules.</strong> The speed of sound in a gas is \(v_s=\sqrt{\gamma RT/M}\). Dividing, \(v_s/v_{rms}=\sqrt{\gamma/3}\). Since γ ≤ 5/3, sound is always slower than the rms speed. For air (γ = 1.4) the ratio is about 0.68.</p>'''),
    ],
    formulas=[
        dict(title='Other forms of the rms speed', formula=r'v_{rms}=\sqrt{\frac{3k_BT}{m}}=\sqrt{\frac{3RT}{M}}=\sqrt{\frac{3P}{\rho}}',
             symbols='k_B = 1.38×10⁻²³ J/K; m mass of one molecule (kg); R = 8.31 J/mol K; M molar mass (kg/mol); T absolute temperature (K); P pressure (Pa); ρ density (kg/m³). Ideal gas in equilibrium.'),
        dict(title='Ratio of the three speeds', formula=r'v_{rms}:\bar v:v_{mp}=\sqrt3:\sqrt{\tfrac{8}{\pi}}:\sqrt2\approx1.73:1.60:1.41',
             symbols='v_rms rms speed, v̄ mean speed, v_mp most probable speed, all in m/s for the same gas at the same temperature. Holds for any ideal gas with a Maxwell distribution.'),
        dict(title='Speed of sound and rms speed', formula=r'v_s=\sqrt{\frac{\gamma RT}{M}}=\sqrt{\frac{\gamma}{3}}\;v_{rms}',
             symbols='v_s speed of sound in the gas (m/s); γ = C_P/C_V (no unit); R = 8.31 J/mol K; T absolute temperature (K); M molar mass (kg/mol). Ideal gas, adiabatic sound waves.'),
    ],
    figure=dict(svg=FIG_MAXWELL,
                caption='Maxwell speed distribution for one gas at T₁ and at T₂ = 2T₁. On the colder curve the three speeds are marked: v_mp at the peak, then v_avg, then v_rms. The hotter curve peaks at a speed √2 times higher and is lower and wider, with the same area.'),
    traps=[
        r'At constant temperature, doubling the pressure leaves \(v_{rms}\) unchanged. The formula \(\sqrt{3P/\rho}\) does not mean \(v_{rms}\propto\sqrt P\), because ρ doubles too.',
        r'To double \(v_{rms}\) you must multiply the <em>kelvin</em> temperature by 4. From 27 °C (300 K) that means 1200 K, which is 927 °C, not 108 °C or 1200 °C.',
        r'(3/2)k_BT is the <em>translational</em> kinetic energy per molecule. For a diatomic gas the total kinetic energy per molecule is larger, (5/2)k_BT, because rotation adds energy.',
    ],
    exam=r'''<ul>
<li>“At what temperature will v_rms of gas X equal that of gas Y at T?” Use T/M = constant.</li>
<li>“v_rms becomes double (or half) when the temperature changes from 27 °C to …”</li>
<li>Ratio v_rms : v̄ : v_mp, or which speed is largest.</li>
<li>Maxwell graph questions: identify the higher temperature or the lighter gas; does the area change; where the peak moves.</li>
<li>“Why is hydrogen rare in Earth’s atmosphere?” or “Why has the Moon no atmosphere?”</li>
<li>Ratio of speed of sound to v_rms for a given γ.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'Find the rms speed of nitrogen molecules (M = 28 g/mol) at 27 °C. Take R = 8.31 J/mol K.',
             steps=[r'Convert: M = 0.028 kg/mol, T = 300 K.',
                    r'\(v_{rms}=\sqrt{\dfrac{3RT}{M}}=\sqrt{\dfrac{3\times8.31\times300}{0.028}}\).',
                    r'\(=\sqrt{2.671\times10^5}\approx517\) m/s.',
                    r'If you forget to convert M and use 28, you get about 16 m/s, which is far too small for a gas at room temperature.'],
             answer=r'About 517 m/s.'),
        dict(tag='Ratio', q=r'At what temperature will the rms speed of hydrogen (M = 2 g/mol) equal the rms speed of oxygen (M = 32 g/mol) at 47 °C?',
             steps=[r'Equal rms speeds need equal T/M.',
                    r'Oxygen: T = 47 + 273 = 320 K, so T/M = 320/32 = 10 K mol/g.',
                    r'Hydrogen: T = 10 × 2 = 20 K.',
                    r'Hydrogen is 16 times lighter, so it needs a 16 times lower kelvin temperature to move as fast.'],
             answer=r'20 K (about −253 °C).'),
        dict(tag='Graph', q=r'Maxwell speed distributions of H₂ and O₂ are drawn at the same temperature. One curve peaks at a low speed and is tall and narrow. The other peaks at a high speed and is low and broad. Which is which, and how far apart are the peaks?',
             steps=[r'At fixed T, \(v_{mp}=\sqrt{2RT/M}\propto1/\sqrt M\).',
                    r'Oxygen is heavier, so its peak is at a lower speed. The total area is the same, so a curve squeezed into a narrower speed range must be taller.',
                    r'The tall, narrow, low-speed curve is O₂. The low, broad curve is H₂.',
                    r'Ratio of peak speeds: \(v_{mp,H_2}/v_{mp,O_2}=\sqrt{32/2}=4\).'],
             answer=r'Tall narrow curve: O₂. Low broad curve: H₂. The H₂ peak is at 4 times the speed of the O₂ peak.'),
        dict(tag='Numerical', q=r'The rms speed of the molecules of a diatomic gas (γ = 1.4) is 500 m/s at some temperature. Find the speed of sound in the gas at that temperature.',
             steps=[r'\(v_s/v_{rms}=\sqrt{\gamma/3}=\sqrt{1.4/3}=\sqrt{0.467}\approx0.683\).',
                    r'\(v_s\approx0.683\times500\approx342\) m/s.',
                    r'Sound is a pressure disturbance carried by the molecules, so it cannot travel faster than the molecules themselves.'],
             answer=r'About 342 m/s.'),
    ],
    practice=[
        dict(type='numerical', q=r'The rms speed of the molecules of a gas at 27 °C is v. The temperature at which it becomes 2v is',
             options=['54 °C', '327 °C', '927 °C', '1200 °C'], answer=2,
             explanation=r'v_rms ∝ √T, so T must become 4 × 300 K = 1200 K = 927 °C. 54 °C doubles the Celsius number, which is meaningless here. 1200 °C forgets to convert the kelvin answer back to Celsius. 327 °C (600 K) only doubles T, which multiplies v_rms by √2.'),
        dict(type='graph', q=r'The Maxwell speed distribution of one gas is drawn at temperatures T₁ and T₂. Curve 2 has its peak at a higher speed, its peak is lower, and it is wider. Which statement is correct?',
             options=['T₂ &lt; T₁, and the area under curve 2 is smaller', 'T₂ &lt; T₁, and both areas are equal', 'T₂ > T₁, and the area under curve 2 is larger', 'T₂ > T₁, and both areas are equal'], answer=3,
             explanation=r'v_mp ∝ √T, so a peak at a higher speed means a higher temperature. The area equals the total number of molecules, which does not change. A lower peak does not mean fewer molecules; the same number is spread over a wider range of speeds.'),
        dict(type='concept', q=r'Hydrogen is very rare in Earth’s atmosphere, while nitrogen is abundant. The best explanation is that',
             options=['Light H₂ molecules have a larger fraction in the high-speed tail above escape speed, so they slowly leak away', 'The rms speed of H₂ at atmospheric temperatures is greater than 11.2 km/s', 'H₂ molecules have less kinetic energy than N₂ molecules at the same temperature', 'Gravity does not act on very light molecules'], answer=0,
             explanation=r'At 300 K the rms speed of H₂ is only about 1.9 km/s, far below 11.2 km/s, so option 2 is false. The escape happens through the fast tail of the distribution, which is much larger for light molecules. At equal T, H₂ and N₂ have equal average translational KE, and gravity acts on all masses.'),
        dict(type='multi', q=r'A fixed mass of ideal gas is compressed isothermally to half its volume. Which of these are correct? (a) v_rms is unchanged. (b) Average kinetic energy per molecule is unchanged. (c) Density doubles. (d) v_rms becomes √2 times.',
             options=['(a) and (b) only', '(a), (b) and (c)', '(c) and (d) only', '(b), (c) and (d)'], answer=1,
             explanation=r'Isothermal means T is fixed, so v_rms = √(3RT/M) and the KE per molecule (3/2)k_BT do not change. Halving the volume doubles the density and the pressure. (d) comes from wrongly using v_rms = √(3P/ρ) with only P doubling.'),
    ],
),
# ---------------------------------------------------------------- equipartition
'kinetic-theory-equipartition': dict(
    level='exam',
    notes=[
        ('The law of equipartition of energy', r'''<p>A molecule can store energy in several independent ways. Each way that adds a squared term to the energy is called a <strong>degree of freedom</strong>. Examples: \(\frac12mv_x^2\) for motion along x, \(\frac12I\omega^2\) for rotation about one axis, and \(\frac12kx^2\) for the stretch of a vibrating bond.</p>
<p>The <strong>law of equipartition</strong> says that in thermal equilibrium at temperature T, each such squared term has the same average energy \(\frac12k_BT\) per molecule.</p>
<ul>
<li>Translation: three terms (x, y, z), so \(\frac32k_BT\). This matches the kinetic theory result for every gas.</li>
<li>If a molecule has f degrees of freedom, its average energy is \(\frac f2k_BT\). One mole has \(\frac f2RT\), and n moles have \(U=\frac f2nRT\).</li>
<li>Ideal-gas molecules do not attract each other, so there is no intermolecular potential energy. U depends only on T, not on P or V.</li>
</ul>'''),
        ('Counting degrees of freedom', r'''<p>A point atom moves in three directions, so N free atoms have 3N coordinates. Every rigid link between atoms removes one. A useful rule is \(f=3N-k\), where k is the number of independent constraints.</p>
<div class="table-wrap"><table>
<thead><tr><th>Molecule</th><th>Translational</th><th>Rotational</th><th>Vibrational</th><th>f</th></tr></thead>
<tbody>
<tr><td>Monatomic (He, Ne, Ar)</td><td>3</td><td>0</td><td>0</td><td>3</td></tr>
<tr><td>Diatomic, rigid (O₂, N₂, H₂ near room T)</td><td>3</td><td>2</td><td>0</td><td>5</td></tr>
<tr><td>Diatomic, vibrating (high T)</td><td>3</td><td>2</td><td>2 (one mode)</td><td>7</td></tr>
<tr><td>Linear triatomic, rigid (CO₂)</td><td>3</td><td>2</td><td>0</td><td>5</td></tr>
<tr><td>Non-linear, rigid (H₂O, NH₃, CH₄)</td><td>3</td><td>3</td><td>0</td><td>6</td></tr>
</tbody></table></div>
<p>A diatomic molecule has only two rotational degrees of freedom. Its moment of inertia about the bond axis is almost zero, so rotation about that axis stores no energy. The same is true for any linear molecule. A non-linear molecule can rotate about all three axes.</p>
<p>One vibrational mode counts twice: once for the kinetic energy of the vibrating atoms and once for the potential energy of the stretched bond.</p>'''),
        ('Where equipartition breaks down', r'''<p>Equipartition is a classical result. Quantum mechanics allows rotational and vibrational energy only in steps. When \(k_BT\) is much smaller than the step size, that mode cannot be excited and contributes nothing: it is “frozen”. Vibrational steps are large, so diatomic vibrations are frozen at room temperature, and f = 5 is the right value there. The next section, on specific heats, shows how this makes heat capacities depend on temperature.</p>'''),
    ],
    formulas=[
        dict(title='Average energy from equipartition', formula=r'\bar\varepsilon=\frac f2k_BT\ \text{per molecule},\qquad U=\frac f2nRT,\qquad f=3N-k',
             symbols='ε̄ average energy per molecule (J); f active degrees of freedom; k_B = 1.38×10⁻²³ J/K; T absolute temperature (K); U internal energy of n moles of ideal gas (J); R = 8.31 J/mol K; N atoms per molecule; k number of independent constraints (rigid bonds). Classical equilibrium.'),
    ],
    traps=[
        r'Translational KE per mole is (3/2)RT for <em>every</em> gas. Total internal energy (f/2)RT depends on the molecule. Read whether a question asks for translational KE, rotational KE or total energy.',
        r'Do not count rotation of a linear molecule about its own axis. A rigid diatomic or CO₂ molecule has f = 5, not 6.',
    ],
    exam=r'''<ul>
<li>“The degrees of freedom of a rigid diatomic (or triatomic, linear or non-linear) molecule are …”</li>
<li>“Find the total (or rotational) kinetic energy of n moles of O₂ at temperature T.”</li>
<li>“What fraction of the energy of a diatomic gas is rotational?” Answer: 2/5.</li>
<li>Match the gas with its f value, often mixed with C_V or γ.</li>
<li>Assertion–reason comparing internal energies of monatomic and diatomic gases at the same temperature.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'Find the total internal energy of 2 mol of oxygen (rigid diatomic) at 27 °C. Split it into translational and rotational parts. Take R = 8.31 J/mol K.',
             steps=[r'Rigid diatomic: f = 5 (3 translational + 2 rotational). T = 300 K.',
                    r'\(U=\frac52nRT=2.5\times2\times8.31\times300=12465\) J ≈ 12.5 kJ.',
                    r'Translational part: \(\frac32nRT=7479\) J.',
                    r'Rotational part: \(\frac22nRT=nRT=4986\) J. The parts add up to the total.'],
             answer=r'U ≈ 12.5 kJ: about 7.48 kJ translational and 4.99 kJ rotational.'),
        dict(tag='Concept', q=r'Count the degrees of freedom of rigid molecules of CO₂ (linear, O=C=O), H₂O (bent) and NH₃ (pyramidal) at ordinary temperatures.',
             steps=[r'Each molecule has 3 translational degrees of freedom.',
                    r'CO₂ is linear. Rotation about its own axis stores no energy, so it has 2 rotational: f = 5.',
                    r'H₂O is bent and NH₃ is pyramidal. They are non-linear, so they rotate about all three axes: f = 3 + 3 = 6.',
                    r'Check H₂O with \(f=3N-k\): N = 3 atoms and k = 3 fixed distances (two O–H bonds and the H–H distance), so f = 9 − 3 = 6.'],
             answer=r'CO₂: 5. H₂O: 6. NH₃: 6.'),
        dict(tag='Concept', q=r'An ideal gas has an internal energy of 3RT per mole at moderate temperatures. What kind of molecule could it be?',
             steps=[r'\(U=\frac f2RT=3RT\) per mole, so f = 6.',
                    r'f = 6 = 3 translational + 3 rotational with no vibration.',
                    r'Three rotational degrees of freedom need a non-linear molecule.'],
             answer=r'A rigid non-linear polyatomic molecule, such as CH₄ or NH₃.'),
    ],
    practice=[
        dict(type='concept', q=r'The average total energy of one molecule of a rigid diatomic ideal gas at temperature T is',
             options=['(3/2)k_BT', 'k_BT', '(5/2)k_BT', '(7/2)k_BT'], answer=2,
             explanation=r'A rigid diatomic molecule has f = 5, so its energy is (5/2)k_BT. (3/2)k_BT is the translational part only. (7/2)k_BT would include a vibrational mode, which is frozen in a rigid molecule.'),
        dict(type='match', q=r'Match each gas in List I with its number of active degrees of freedom in List II. List I: (A) He, (B) N₂, rigid, (C) N₂ with vibration active, (D) NH₃, rigid. List II: (1) 6, (2) 3, (3) 7, (4) 5.',
             options=['A-2, B-4, C-1, D-3', 'A-3, B-4, C-2, D-1', 'A-2, B-1, C-3, D-4', 'A-2, B-4, C-3, D-1'], answer=3,
             explanation=r'He is monatomic: 3. Rigid N₂: 3 + 2 = 5. Vibration adds 2 more (kinetic and potential): 7. NH₃ is non-linear, so 3 + 3 = 6. Option 3 gives N₂ six degrees of freedom by counting rotation about the bond axis.'),
        dict(type='ar', q=r'Assertion (A): At the same temperature, one mole of O₂ has more internal energy than one mole of He. Reason (R): The average translational kinetic energy of a molecule depends only on the temperature.',
             options=['Both A and R are true and R is the correct explanation of A', 'Both A and R are true but R is not the correct explanation of A', 'A is true but R is false', 'A is false but R is true'], answer=1,
             explanation=r'A is true: O₂ has (5/2)RT per mole and He has (3/2)RT. R is also true. But R says translational energies are equal, so it cannot explain the difference. The difference comes from the two rotational degrees of freedom of O₂.'),
        dict(type='numerical', q=r'For one mole of a rigid diatomic ideal gas at temperature T, the ratio of rotational kinetic energy to translational kinetic energy is',
             options=['2 : 3', '3 : 2', '2 : 5', '1 : 1'], answer=0,
             explanation=r'Rotational energy is (2/2)RT = RT and translational is (3/2)RT, so the ratio is 2 : 3. 2 : 5 is rotational energy as a fraction of the total. 3 : 2 is the inverse ratio.'),
    ],
),
# ---------------------------------------------------------------- mixtures
'kinetic-theory-mixtures': dict(
    notes=[
        ('Dalton’s law from kinetic theory', r'''<p>In an ideal gas the molecules do not exert forces on each other between collisions. So each gas in a mixture hits the walls exactly as it would if it were alone in the container. Its pressure is \(P_i=\frac13\rho_iv_{rms,i}^2=n_iRT/V\), and the total pressure is the sum of these partial pressures.</p>
<p>All the gases share one temperature, so they share the same average translational kinetic energy per molecule, \(\frac32k_BT\). Their rms speeds still differ: the lighter gas moves faster.</p>
<p>The partial pressure fraction equals the <em>mole</em> fraction. If masses are given, divide each by its molar mass first.</p>'''),
        ('Molar mass and density of a mixture', r'''<p>A mixture behaves like a single ideal gas with an average molar mass, total mass divided by total moles:</p>
<p>\[M_{mix}=\frac{n_1M_1+n_2M_2}{n_1+n_2}\]</p>
<p>Example: dry air is roughly 79% N₂ and 21% O₂ by moles, so \(M_{mix}\approx0.79\times28+0.21\times32\approx28.8\) g/mol. The mixture density is then \(\rho=PM_{mix}/(RT)\).</p>'''),
        ('Mixing gases from two containers', r'''<p>Two containers are joined by a thin tube and no gas escapes. Moles are conserved: \(\dfrac{PV_{total}}{RT}=\dfrac{P_1V_1}{RT_1}+\dfrac{P_2V_2}{RT_2}\).</p>
<ul>
<li>If both start at the same temperature and it stays fixed, the final pressure is \(P=\dfrac{P_1V_1+P_2V_2}{V_1+V_2}\).</li>
<li>If the system is insulated and does no work, the total internal energy is conserved: \(\frac{f_1}{2}n_1RT_1+\frac{f_2}{2}n_2RT_2=\left(\frac{f_1}{2}n_1+\frac{f_2}{2}n_2\right)RT\). So \(T=\dfrac{f_1n_1T_1+f_2n_2T_2}{f_1n_1+f_2n_2}\). For the same kind of gas this becomes \(T=\dfrac{n_1T_1+n_2T_2}{n_1+n_2}\).</li>
</ul>'''),
        ('Energy and heat capacity of a mixture', r'''<p>Internal energies add, so the mixture has \(U=\frac{f_1}{2}n_1RT+\frac{f_2}{2}n_2RT\). Writing this as \(\frac{f_{mix}}{2}(n_1+n_2)RT\) gives</p>
<p>\[f_{mix}=\frac{n_1f_1+n_2f_2}{n_1+n_2},\qquad C_{V,mix}=\frac{n_1C_{V1}+n_2C_{V2}}{n_1+n_2},\qquad C_{P,mix}=C_{V,mix}+R\]</p>
<p>Since \(C_V=R/(\gamma-1)\), the same weighting gives \(\dfrac{n_1+n_2}{\gamma_{mix}-1}=\dfrac{n_1}{\gamma_1-1}+\dfrac{n_2}{\gamma_2-1}\). Never average the γ values directly. The specific heats section has a worked example.</p>'''),
    ],
    formulas=[
        dict(title='Average molar mass of a mixture', formula=r'M_{mix}=\frac{n_1M_1+n_2M_2}{n_1+n_2}=\frac{m_1+m_2}{\dfrac{m_1}{M_1}+\dfrac{m_2}{M_2}}',
             symbols='M_mix effective molar mass (kg/mol or g/mol, consistently); n₁, n₂ moles of each gas; M₁, M₂ molar masses; m₁, m₂ masses of each gas. Ideal non-reacting mixture.'),
        dict(title='Temperature after insulated mixing', formula=r'T=\frac{f_1n_1T_1+f_2n_2T_2}{f_1n_1+f_2n_2}',
             symbols='T final common temperature (K); f₁, f₂ degrees of freedom; n₁, n₂ moles; T₁, T₂ initial temperatures (K). No heat exchange with the surroundings and no external work; ideal gases.'),
        dict(title='γ of a mixture', formula=r'\frac{n_1+n_2}{\gamma_{mix}-1}=\frac{n_1}{\gamma_1-1}+\frac{n_2}{\gamma_2-1}',
             symbols='γ_mix, γ₁, γ₂ ratios C_P/C_V (no unit); n₁, n₂ moles of each gas. Follows from adding the C_V values; ideal non-reacting gases.'),
    ],
    traps=[
        r'Same temperature means the same average translational KE per molecule, not the same rms speed, not the same partial pressure and not the same momentum.',
        r'When two gas samples at different temperatures mix, the final temperature is not the simple average unless the samples have the same number of moles and the same f. Weight each temperature by f·n.',
    ],
    exam=r'''<ul>
<li>Partial pressures from given masses (convert masses to moles first).</li>
<li>Average molar mass of a mixture, or the density of air.</li>
<li>Two vessels connected by a tube: final pressure and temperature.</li>
<li>γ or C_V of a mixture of a monatomic and a diatomic gas.</li>
<li>Dissociation questions: count particles again before using P ∝ NT.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'A vessel contains 8 g of O₂ and 14 g of N₂. The total pressure is 3 atm. Find each partial pressure and the average molar mass of the mixture.',
             steps=[r'Moles: O₂ = 8/32 = 0.25 mol; N₂ = 14/28 = 0.5 mol. Total = 0.75 mol.',
                    r'Mole fractions: O₂ = 0.25/0.75 = 1/3; N₂ = 2/3.',
                    r'Partial pressures: O₂ = 3 × 1/3 = 1 atm; N₂ = 3 × 2/3 = 2 atm.',
                    r'\(M_{mix}=(8+14)/0.75\approx29.3\) g/mol.'],
             answer=r'p(O₂) = 1 atm, p(N₂) = 2 atm, M_mix ≈ 29.3 g/mol.'),
        dict(tag='Numerical', q=r'Vessel A (2 L) holds a gas at 3 atm. Vessel B (3 L) holds the same gas at 2 atm. Both are at the same temperature. They are connected by a thin tube and the temperature stays the same. Find the final pressure.',
             steps=[r'At constant T, moles ∝ PV, and moles are conserved.',
                    r'\(P(V_A+V_B)=P_AV_A+P_BV_B=3\times2+2\times3=12\) atm L.',
                    r'\(P=12/5=2.4\) atm.'],
             answer=r'2.4 atm.'),
        dict(tag='Numerical', q=r'In an insulated rigid container, 1 mol of helium at 500 K is mixed with 1 mol of oxygen (rigid diatomic) at 300 K. Find the final temperature.',
             steps=[r'No heat enters and no work is done, so total internal energy is conserved.',
                    r'Helium: f = 3. Oxygen: f = 5.',
                    r'\(T=\dfrac{3\times1\times500+5\times1\times300}{3\times1+5\times1}=\dfrac{1500+1500}{8}=375\) K.',
                    r'The simple average would be 400 K. The answer is lower because oxygen needs more energy per kelvin, so it pulls the final temperature towards its own.'],
             answer=r'375 K.'),
    ],
    practice=[
        dict(type='numerical', q=r'A container holds 4 g of helium (M = 4 g/mol) and 16 g of oxygen (M = 32 g/mol). The total pressure is 1.5 atm. The partial pressure of helium is',
             options=['1.0 atm', '0.5 atm', '0.3 atm', '1.2 atm'], answer=0,
             explanation=r'Helium: 1 mol. Oxygen: 0.5 mol. The mole fraction of He is 1/1.5 = 2/3, so p(He) = 1.0 atm. 0.3 atm uses the mass fraction 4/20. 0.5 atm is the oxygen partial pressure.'),
        dict(type='numerical', q=r'2 mol of a monatomic ideal gas is mixed with 3 mol of a rigid diatomic ideal gas. The ratio γ = C_P/C_V for the mixture is',
             options=['113/75 ≈ 1.51', '31/21 ≈ 1.48', '7/5 = 1.40', '5/3 ≈ 1.67'], answer=1,
             explanation=r'C_V,mix = (2 × 3R/2 + 3 × 5R/2)/5 = 2.1R, so C_P,mix = 3.1R and γ = 3.1/2.1 = 31/21. 113/75 comes from averaging the two γ values directly, which is wrong. 1.40 and 1.67 are the γ values of the pure gases.'),
        dict(type='ar', q=r'Assertion (A): The total pressure of a mixture of ideal gases equals the sum of the partial pressures of its components. Reason (R): Molecules of different gases attract each other strongly, so they move together.',
             options=['Both A and R are true and R is the correct explanation of A', 'Both A and R are true but R is not the correct explanation of A', 'A is true but R is false', 'A is false but R is true'], answer=2,
             explanation=r'Dalton’s law (A) holds for ideal gases. It holds precisely because ideal-gas molecules do not attract each other, so each gas acts as if alone. R contradicts the ideal-gas model, so R is false.'),
        dict(type='concept', q=r'A mixture of H₂ and O₂ is in thermal equilibrium. Which quantity is the same for the two kinds of molecules?',
             options=['Rms speed', 'Partial pressure', 'Average momentum magnitude', 'Average translational kinetic energy'], answer=3,
             explanation=r'Equal temperature means equal average translational KE, (3/2)k_BT. Rms speed is 4 times larger for H₂. Partial pressures depend on the mole amounts, which are not given. Momentum √(2mK) is larger for the heavier O₂ molecule.'),
    ],
),
# ---------------------------------------------------------------- mean free path
'kinetic-theory-mean-free-path': dict(
    notes=[
        ('Derivation: the collision cylinder', r'''<p>Perfume molecules move at hundreds of metres per second, yet the smell takes many seconds to cross a room. The reason is collisions: each molecule zig-zags, changing direction billions of times every second.</p>
<ol>
<li>Treat molecules as hard spheres of diameter d. Two molecules collide if their centres come within a distance d of each other.</li>
<li>Let one molecule move with average speed \(\bar v\) and imagine the others at rest. In time t it sweeps out a cylinder of radius d and length \(\bar vt\). Its volume is \(\pi d^2\bar vt\).</li>
<li>Every molecule whose centre lies inside this cylinder is hit. With \(n_N\) molecules per unit volume, the number of collisions is \(n_N\pi d^2\bar vt\).</li>
<li>Mean free path = distance travelled ÷ number of collisions = \(\dfrac{\bar vt}{n_N\pi d^2\bar vt}=\dfrac{1}{\pi d^2n_N}\).</li>
<li>The other molecules are moving too. The average relative speed is \(\sqrt2\,\bar v\), so there are \(\sqrt2\) times more collisions. This gives \(\lambda=\dfrac{1}{\sqrt2\pi d^2n_N}\).</li>
</ol>
<p>The quantity \(\pi d^2\) is the collision cross-section. It uses the diameter, not the radius. If a question gives radius r, use \(\pi d^2=4\pi r^2\).</p>'''),
        ('How λ and collision frequency depend on T and P', r'''<p>Using \(n_N=P/(k_BT)\), \(\lambda=\dfrac{k_BT}{\sqrt2\pi d^2P}\). The collision frequency (collisions per second for one molecule) is \(\nu=\bar v/\lambda=\sqrt2\pi d^2n_N\bar v\), and the mean time between collisions is \(\tau=1/\nu\).</p>
<div class="table-wrap"><table>
<thead><tr><th>Condition</th><th>Mean free path λ</th><th>Collision frequency ν</th></tr></thead>
<tbody>
<tr><td>Fixed V and N (sealed rigid box), T rises</td><td>unchanged</td><td>∝ √T</td></tr>
<tr><td>Fixed P, T rises</td><td>∝ T</td><td>∝ 1/√T</td></tr>
<tr><td>Fixed T, P rises</td><td>∝ 1/P</td><td>∝ P</td></tr>
<tr><td>Larger molecules</td><td>∝ 1/d²</td><td>∝ d²</td></tr>
</tbody></table></div>
<p>For air at room conditions, λ is about 10⁻⁷ m. This is roughly 300 molecular diameters and about 30 times the average spacing between molecules. A molecule collides about 5×10⁹ times per second.</p>'''),
    ],
    formulas=[
        dict(title='Collision frequency and mean free time', formula=r'\nu=\frac{\bar v}{\lambda}=\sqrt2\,\pi d^2n_N\bar v,\qquad \tau=\frac1\nu=\frac{\lambda}{\bar v}',
             symbols='ν collisions per second for one molecule (s⁻¹); v̄ mean speed (m/s); λ mean free path (m); d molecular diameter (m); n_N number density (m⁻³); τ mean time between collisions (s). Hard-sphere ideal gas.'),
    ],
    figure=dict(svg=FIG_CYLINDER,
                caption='A molecule of diameter d moving through the gas sweeps out a cylinder of radius d. Any molecule whose centre lies inside the cylinder is struck. The cylinder volume πd²v̄t times the number density gives the number of collisions.'),
    traps=[
        r'The cross-section is πd², with d the <em>diameter</em>. Using πr² underestimates the collision rate four times.',
        r'Mean free path is not the average gap between neighbouring molecules. In a gas at room conditions the gap is a few nanometres, while λ is about 100 nm.',
    ],
    exam=r'''<ul>
<li>“The mean free path of a gas is λ. If pressure is doubled at constant temperature, it becomes …”</li>
<li>“Two gases have diameters d and 2d …”: compare mean free paths or collision frequencies.</li>
<li>Graph: λ against T at constant P (straight line through origin), λ against P at constant T (hyperbola).</li>
<li>Statements about a gas heated in a sealed rigid container: λ unchanged, collision frequency up.</li>
<li>Direct substitution in λ = k_BT/(√2πd²P) with given T, P and d.</li>
</ul>''',
    examples=[
        dict(tag='Numerical', q=r'Estimate the mean free path and collision frequency of nitrogen molecules (d = 3.0×10⁻¹⁰ m, M = 28 g/mol) at 300 K and 1.0×10⁵ Pa. Take k_B = 1.38×10⁻²³ J/K and R = 8.31 J/mol K.',
             steps=[r'\(\lambda=\dfrac{k_BT}{\sqrt2\pi d^2P}=\dfrac{1.38\times10^{-23}\times300}{1.414\times3.1416\times9.0\times10^{-20}\times10^5}\).',
                    r'Numerator = 4.14×10⁻²¹. Denominator ≈ 4.0×10⁻¹⁴. So \(\lambda\approx1.0\times10^{-7}\) m.',
                    r'Mean speed: \(\bar v=\sqrt{8RT/(\pi M)}=\sqrt{8\times8.31\times300/(3.1416\times0.028)}\approx476\) m/s.',
                    r'\(\nu=\bar v/\lambda\approx476/(1.04\times10^{-7})\approx4.6\times10^9\) s⁻¹.'],
             answer=r'λ ≈ 1.0×10⁻⁷ m; about 4.6×10⁹ collisions per second.'),
        dict(tag='Ratio', q=r'A gas is heated from 300 K to 600 K at constant pressure. How do its mean free path, mean speed and collision frequency change?',
             steps=[r'At constant P, \(\lambda\propto T\): λ doubles.',
                    r'\(\bar v\propto\sqrt T\): mean speed becomes √2 times.',
                    r'\(\nu=\bar v/\lambda\): it changes by \(\sqrt2/2=1/\sqrt2\).',
                    r'The gas has expanded and become less dense. Molecules move faster but meet each other less often.'],
             answer=r'λ doubles, v̄ becomes √2 times, ν becomes 1/√2 times (about 0.71).'),
        dict(tag='Concept', q=r'For a gas at 300 K and 10⁵ Pa, compare the average distance between neighbouring molecules with the mean free path of about 1.0×10⁻⁷ m.',
             steps=[r'Number density \(n_N=P/(k_BT)=10^5/(1.38\times10^{-23}\times300)\approx2.4\times10^{25}\) m⁻³.',
                    r'Each molecule has a volume \(1/n_N\) to itself. Average spacing ≈ \(n_N^{-1/3}\approx3.5\times10^{-9}\) m.',
                    r'Ratio λ / spacing ≈ 1.0×10⁻⁷ / 3.5×10⁻⁹ ≈ 30.',
                    r'Molecules are small compared with their spacing, so a molecule usually passes many neighbours before it actually hits one.'],
             answer=r'Spacing ≈ 3.5 nm, about 30 times smaller than the mean free path.'),
    ],
    practice=[
        dict(type='numerical', q=r'Gas A has molecular diameter d and is at pressure P. Gas B has molecular diameter 2d and is at pressure P/2. Both are at the same temperature. The ratio λ_B/λ_A of their mean free paths is',
             options=['1', '1/2', '2', '1/4'], answer=1,
             explanation=r'λ ∝ 1/(d²P) at fixed T. λ_B/λ_A = 1/(4 × 1/2) = 1/2. 1/4 ignores the lower pressure of B. 2 inverts the dependence on pressure.'),
        dict(type='graph', q=r'For a fixed mass of ideal gas at constant pressure, a graph of mean free path (y-axis) against absolute temperature (x-axis) is',
             options=['A rectangular hyperbola', 'A horizontal straight line', 'A parabola through the origin', 'A straight line through the origin'], answer=3,
             explanation=r'λ = k_BT/(√2πd²P), so at fixed P, λ ∝ T: a straight line through the origin. The horizontal line applies at fixed volume. The hyperbola is λ against P at fixed T.'),
        dict(type='statement', q=r'An ideal gas in a sealed rigid container is heated. Statement I: The mean free path of the molecules does not change. Statement II: The number of collisions per second made by each molecule increases.',
             options=['Both statements are correct', 'Both statements are incorrect', 'Statement I is correct but Statement II is incorrect', 'Statement I is incorrect but Statement II is correct'], answer=0,
             explanation=r'λ depends on number density, which is fixed in a sealed rigid container, so Statement I is correct. ν = v̄/λ and v̄ ∝ √T, so collisions become more frequent and Statement II is correct. A common error is to use λ ∝ T, which holds only at constant pressure.'),
        dict(type='numerical', q=r'At constant temperature the pressure of a gas is doubled. The collision frequency of a molecule',
             options=['halves', 'stays the same', 'doubles', 'becomes four times'], answer=2,
             explanation=r'At fixed T, n_N ∝ P, so λ halves while v̄ stays the same. ν = v̄/λ therefore doubles. “Stays the same” forgets the change in density. Four times wrongly squares the pressure factor.'),
    ],
),
}

NEW_SECTIONS = [
dict(chapter='kinetic-theory', after='kinetic-theory-equipartition', id='kinetic-theory-specific-heats',
     title='Specific heats of gases and Mayer’s relation',
     intro=r'A gas has no single heat capacity. The heat needed to warm it by 1 K depends on what happens to its volume. At constant volume, all the heat goes into internal energy. At constant pressure, the gas also expands and pushes on its surroundings, so more heat is needed for the same rise in temperature.',
     reasoning=r'Molar heat capacity C is heat per mole per kelvin; specific heat c is heat per kilogram per kelvin, so C = Mc. For an ideal gas, internal energy depends only on temperature, so the same ΔT gives the same ΔU in both processes. The extra heat at constant pressure is the expansion work PΔV = nRΔT, which gives Mayer’s relation C_P − C_V = R.',
     formula=r'C_P-C_V=R,\qquad c_p-c_v=\frac{R}{M},\qquad \gamma=\frac{C_P}{C_V}=1+\frac{2}{f}',
     symbols='C_P, C_V molar heat capacities at constant pressure and constant volume (J/mol K); c_p, c_v specific heats (J/kg K); R = 8.31 J/mol K; M molar mass (kg/mol); γ ratio of heat capacities (no unit); f active degrees of freedom. Ideal gas.',
     trap=r'Mayer’s relation is per mole. Per kilogram the difference is R/M, which is different for every gas.',
     example=r'For an ideal gas γ = 1.4. Find C_V and C_P, taking R = 8.31 J/mol K.',
     solution=r'C_V = R/(γ − 1) = 8.31/0.4 ≈ 20.8 J/mol K. C_P = γC_V ≈ 29.1 J/mol K. Their difference is R, as Mayer’s relation requires.',
     question=r'For hydrogen (M = 2 g/mol) and oxygen (M = 32 g/mol), the ratio of (c_p − c_v) per kilogram, hydrogen to oxygen, is',
     options='1 : 1|1 : 4|16 : 1|4 : 1', answer=2,
     explanation=r'Per kilogram, c_p − c_v = R/M. The ratio is 32/2 = 16, so hydrogen’s value is 16 times larger. 1 : 1 holds only per mole. 4 : 1 wrongly takes a square root, as for rms speeds.',
     deep=dict(
        level='exam',
        notes=[
            ('Why a gas has many heat capacities', r'''<p>Heat capacity is \(C=\dfrac{Q}{n\Delta T}\), and Q depends on the process. Two processes are standard:</p>
<ul>
<li><strong>Constant volume:</strong> no work is done, so \(Q=\Delta U=nC_V\Delta T\). For an ideal gas, \(C_V=\dfrac f2R\).</li>
<li><strong>Constant pressure:</strong> the gas expands and does work, so \(C_P>C_V\).</li>
</ul>
<p>Other processes give other values. In an isothermal process heat flows in but ΔT = 0, so C is infinite. In an adiabatic process Q = 0 while T changes, so C = 0. A process can even have a negative heat capacity. Per-mole and per-kilogram values are related by \(C=Mc\).</p>'''),
            ('Derivation of Mayer’s relation', r'''<ol>
<li>Heat n moles of ideal gas at constant volume through ΔT: \(Q_V=nC_V\Delta T=\Delta U\).</li>
<li>Heat the same gas through the same ΔT at constant pressure: \(Q_P=nC_P\Delta T=\Delta U+P\Delta V\).</li>
<li>ΔU depends only on ΔT for an ideal gas, so it is the same in both cases: \(\Delta U=nC_V\Delta T\).</li>
<li>At constant P, \(P\Delta V=nR\Delta T\) from PV = nRT.</li>
<li>So \(nC_P\Delta T=nC_V\Delta T+nR\Delta T\), giving \(C_P-C_V=R\).</li>
</ol>
<p>The same steps show how heat supplied at constant pressure is shared: the fraction going into internal energy is \(\dfrac{\Delta U}{Q}=\dfrac{C_V}{C_P}=\dfrac1\gamma\), and the fraction turned into work is \(\dfrac{W}{Q}=1-\dfrac1\gamma=\dfrac{2}{f+2}\). For a diatomic gas these are 5/7 and 2/7.</p>'''),
            ('Standard values', r'''<div class="table-wrap"><table>
<thead><tr><th>Gas type</th><th>f</th><th>C_V</th><th>C_P</th><th>γ</th></tr></thead>
<tbody>
<tr><td>Monatomic (He, Ar)</td><td>3</td><td>3R/2</td><td>5R/2</td><td>5/3 ≈ 1.67</td></tr>
<tr><td>Diatomic, rigid (O₂, N₂ at room T); linear CO₂, rigid</td><td>5</td><td>5R/2</td><td>7R/2</td><td>7/5 = 1.40</td></tr>
<tr><td>Non-linear polyatomic, rigid (CH₄, NH₃)</td><td>6</td><td>3R</td><td>4R</td><td>4/3 ≈ 1.33</td></tr>
<tr><td>Diatomic with vibration (high T)</td><td>7</td><td>7R/2</td><td>9R/2</td><td>9/7 ≈ 1.29</td></tr>
</tbody></table></div>
<p>Since \(\gamma=1+2/f\), more degrees of freedom mean a smaller γ. γ always lies between 1 and 5/3 for an ideal gas. Useful inverses: \(C_V=\dfrac{R}{\gamma-1}\) and \(C_P=\dfrac{\gamma R}{\gamma-1}\).</p>
<p><strong>Mixtures in one line.</strong> C_V values add with mole weights, so \(\dfrac{n_1+n_2}{\gamma_{mix}-1}=\dfrac{n_1}{\gamma_1-1}+\dfrac{n_2}{\gamma_2-1}\). The mixtures section derives this; never average γ directly.</p>'''),
            ('Temperature dependence and solids', r'''<p>Heat capacities are not fixed numbers. For hydrogen gas, C_V is about 3R/2 at very low temperature, because rotations are frozen. It rises to 5R/2 near room temperature when rotations switch on, and towards 7R/2 at a few thousand kelvin when vibration switches on. Classical equipartition cannot explain these steps; quantum theory does.</p>
<p><strong>Solids (Dulong–Petit law).</strong> Each atom in a solid vibrates about a fixed point in three directions. Each direction has a kinetic and a potential energy term, so there are 6 squared terms and an energy of \(3k_BT\) per atom. One mole has \(U=3RT\), so \(C=3R\approx25\) J/mol K. For a solid, C_P ≈ C_V because its expansion work is tiny. This value holds at ordinary and high temperatures; at low temperatures the heat capacity falls towards zero.</p>'''),
        ],
        formulas=[
            dict(title='C_V and C_P from γ', formula=r'C_V=\frac{R}{\gamma-1},\qquad C_P=\frac{\gamma R}{\gamma-1}',
                 symbols='C_V, C_P molar heat capacities (J/mol K); R = 8.31 J/mol K; γ = C_P/C_V (no unit). Ideal gas; follows from Mayer’s relation.'),
            dict(title='Sharing of heat at constant pressure', formula=r'\frac{\Delta U}{Q}=\frac1\gamma,\qquad \frac{W}{Q}=1-\frac1\gamma=\frac{2}{f+2}',
                 symbols='Q heat supplied at constant pressure (J); ΔU rise in internal energy (J); W work done by the gas (J); γ = C_P/C_V; f degrees of freedom. Ideal gas, isobaric process.'),
            dict(title='Dulong–Petit law for solids', formula=r'C\approx3R\approx25\ \text{J mol}^{-1}\text{K}^{-1}',
                 symbols='C molar heat capacity of a solid element (J/mol K); R = 8.31 J/mol K. Each atom is a 3D oscillator with 6 squared energy terms. Valid at ordinary and high temperatures; fails at low temperatures.'),
        ],
        figure=dict(svg=FIG_CV_H2,
                    caption='Molar heat capacity C_V of hydrogen gas against temperature (log scale, qualitative). It rises in steps as rotation and then vibration become active. Near room temperature H₂ behaves as a rigid diatomic gas with C_V = 5R/2.'),
        traps=[
            r'γ of a mixture is not the mole-weighted average of the γ values. Average the C_V values (or 1/(γ − 1)), then find γ.',
            r'C_P − C_V = R is for ideal gases. For solids and liquids C_P ≈ C_V, because their expansion work is very small.',
            r'If a question gives specific heats in J/kg K, Mayer’s relation becomes c_p − c_v = R/M, with M in kg/mol.',
        ],
        exam=r'''<ul>
<li>“For a gas γ = … Find C_V, C_P, or the degrees of freedom.”</li>
<li>“What fraction of heat supplied at constant pressure goes into work (or internal energy)?” Answer: 1 − 1/γ (or 1/γ).</li>
<li>Given c_p and c_v in J/kg K, find the molar mass and identify the gas.</li>
<li>γ of a mixture of a monatomic and a diatomic gas.</li>
<li>Statement questions on how C_V changes with temperature, or the Dulong–Petit value 3R for solids.</li>
</ul>''',
        examples=[
            dict(tag='Numerical', q=r'1 mol of helium is mixed with 1 mol of oxygen (rigid diatomic). Find γ of the mixture.',
                 steps=[r'\(C_{V,mix}=\dfrac{1\times\frac32R+1\times\frac52R}{2}=2R\).',
                        r'\(C_{P,mix}=C_{V,mix}+R=3R\).',
                        r'\(\gamma_{mix}=3R/2R=1.5\).',
                        r'Check with the γ rule: \(\dfrac{2}{\gamma-1}=\dfrac{1}{2/3}+\dfrac{1}{0.4}=1.5+2.5=4\), so γ − 1 = 0.5. The plain average of 5/3 and 7/5 would give about 1.53.'],
                 answer=r'γ = 1.5.'),
            dict(tag='Numerical', q=r'2 mol of nitrogen (rigid diatomic) is heated at constant pressure from 300 K to 310 K. Find the heat supplied, the rise in internal energy and the work done by the gas. Take R = 8.31 J/mol K.',
                 steps=[r'C_P = 7R/2 and C_V = 5R/2.',
                        r'\(Q=nC_P\Delta T=2\times3.5\times8.31\times10\approx582\) J.',
                        r'\(\Delta U=nC_V\Delta T=2\times2.5\times8.31\times10\approx416\) J.',
                        r'\(W=Q-\Delta U=nR\Delta T=2\times8.31\times10\approx166\) J. Check: W/Q = 2/7.'],
                 answer=r'Q ≈ 582 J, ΔU ≈ 416 J, W ≈ 166 J.'),
            dict(tag='Numerical', q=r'A gas has c_p = 14.3 kJ/kg K and c_v = 10.2 kJ/kg K. Find its molar mass and identify the gas. Take R = 8.31 J/mol K.',
                 steps=[r'Per kilogram, \(c_p-c_v=R/M\).',
                        r'\(c_p-c_v=4.1\times10^3\) J/kg K.',
                        r'\(M=8.31/4100\approx2.0\times10^{-3}\) kg/mol = 2 g/mol.',
                        r'γ = 14.3/10.2 ≈ 1.40, which fits a diatomic gas.'],
                 answer=r'M ≈ 2 g/mol, so the gas is hydrogen (H₂).'),
            dict(tag='Numerical', q=r'Use the Dulong–Petit law to estimate the specific heat of aluminium (M = 27 g/mol).',
                 steps=[r'Molar heat capacity of a solid ≈ 3R = 3 × 8.31 ≈ 24.9 J/mol K.',
                        r'Specific heat c = C/M = 24.9/0.027.',
                        r'c ≈ 923 J/kg K. The measured value is about 900 J/kg K, so the estimate is good at room temperature.'],
                 answer=r'About 9.2×10² J/kg K.'),
        ],
        practice=[
            dict(type='numerical', q=r'Heat Q is given to a rigid diatomic ideal gas at constant pressure. The fraction of Q converted into work done by the gas is',
                 options=['2/7', '5/7', '2/5', '3/5'], answer=0,
                 explanation=r'W/Q = nRΔT/(nC_PΔT) = R/(7R/2) = 2/7. 5/7 is the fraction that goes into internal energy. 2/5 uses C_V in place of C_P in the denominator.'),
            dict(type='numerical', q=r'For nitrogen (M = 28 g/mol), γ = 1.4. Its specific heat at constant volume c_v, with R = 8.31 J/mol K, is about',
                 options=['20.8 J/kg K', '742 J/kg K', '1039 J/kg K', '297 J/kg K'], answer=1,
                 explanation=r'C_V = R/(γ − 1) = 20.8 J/mol K. Divide by M = 0.028 kg/mol: c_v ≈ 742 J/kg K. 20.8 is the molar value. 1039 J/kg K is c_p. 297 J/kg K is R/M, the difference c_p − c_v.'),
            dict(type='statement', q=r'Statement I: For every ideal gas, monatomic or polyatomic, C_P − C_V = R per mole. Statement II: For every ideal gas, the difference c_p − c_v per kilogram is also the same.',
                 options=['Both statements are correct', 'Both statements are incorrect', 'Statement I is incorrect but Statement II is correct', 'Statement I is correct but Statement II is incorrect'], answer=3,
                 explanation=r'Mayer’s derivation uses only PΔV = nRΔT, which holds for every ideal gas, so Statement I is correct. Per kilogram the difference is R/M, which depends on the gas, so Statement II is incorrect.'),
            dict(type='graph', q=r'The molar heat capacity C_V of hydrogen gas is measured from very low temperatures up to several thousand kelvin. The graph shows',
                 options=['A fall from 7R/2 to 5R/2 to 3R/2 as T increases', 'A constant value 5R/2 at all temperatures', 'A rise from 3R/2 to 5R/2 to 7R/2 as T increases', 'A constant value 3R, as for solids'], answer=2,
                 explanation=r'At low T only translation is active (3R/2). Rotation switches on at moderate temperatures (5R/2) and vibration at very high temperatures (7R/2). 5R/2 is correct only near room temperature. 3R is the Dulong–Petit value for solids.'),
        ],
     )),
]
