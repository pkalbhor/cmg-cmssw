from CMGTools.WMass.analyzers.CoreTreeProducer import *

# def fillMuonCovMatrix( tree, pName, covMatrix,event ):
    # for i in range(0,9):
        # # tree.vars['{pName}CovMatrix'.format(pName=pName)][i] = covMatrix[i]
        # # if self.scalar:
            # # for i,w in enumerate(event.pdfWeights[pdf]):
                # # tr.fill('pdfWeight_%s_%d' % (pdf,i), w)
                # tree.fill('{pName}CovMatrix'.format(pName=pName), covMatrix[i])
        # # else:
            # # tr.vfill('pdfWeight_%s' % pdf, event.pdfWeights[pdf])

class WTreeProducer( TreeAnalyzerNumpy ):
    
    MuonClass = Muon 

    
    def declareHandles(self):
      super(WTreeProducer, self).declareHandles()
    
      self.handles['pfMet'] = AutoHandle('cmgPFMET','std::vector<cmg::BaseMET>')
      self.handles['pfMetraw'] = AutoHandle('cmgPFMETRaw','std::vector<cmg::BaseMET>')
      self.handles['pfMetSignificance'] = AutoHandle('pfMetSignificance','cmg::METSignificance')
      self.handles['nopuMet'] = AutoHandle('nopuMet','std::vector<reco::PFMET>')
      self.handles['pucMet'] = AutoHandle('pcMet','std::vector<reco::PFMET>')
      self.handles['pfMetForRegression'] = AutoHandle('pfMetForRegression','std::vector<reco::PFMET>')
      self.handles['puMet'] = AutoHandle('puMet','std::vector<reco::PFMET>')
      self.handles['tkMet'] = AutoHandle('tkMet','std::vector<reco::PFMET>')
      
      self.handles['muons'] = AutoHandle(
            'cmgMuonSel',
            'std::vector<cmg::Muon>'
            )
      self.handles['electrons'] = AutoHandle(
            'cmgElectronSel',
            'std::vector<cmg::Electron>'
            )
      self.mchandles['genParticles'] = AutoHandle( 'genParticlesPruned',
            'std::vector<reco::GenParticle>' )
    
      self.handles['vertices'] =  AutoHandle(
          # 'offlinePrimaryVertices',
          'slimmedPrimaryVertices',
          'std::vector<reco::Vertex>'
          )
      self.mchandles['pusi'] =  AutoHandle(
          'addPileupInfo',
          'std::vector<PileupSummaryInfo>' 
          ) 
      self.mchandles['generator'] = AutoHandle(
          'generator','GenEventInfoProduct' 
          )
    
    def declareVariables(self):
      tr = self.tree
      
      if (self.cfg_comp.isMC):
        var(tr, 'scalePDF')
        var(tr, 'parton1_pdgId')
        var(tr, 'parton1_x')
        var(tr, 'parton2_pdgId')
        var(tr, 'parton2_x')

      var( tr, 'run', int)
      var( tr, 'lumi', int)
      var( tr, 'evt', int)
      var( tr, 'nvtx', int)
      var( tr, 'njets', int)
      var( tr, 'npu', int)
      var( tr, 'evtHasGoodVtx', int)
      var( tr, 'Vtx_ndof', int)
      # var( tr, 'firstVtxIsGood', int)
      var( tr, 'evtHasTrg', int)
      var( tr, 'evtWSel', int)
      
      var( tr, 'nMuons', int)
      var( tr, 'nTrgMuons', int)
      var( tr, 'noTrgMuonsLeadingPt', int)

      bookCustomMET( tr, 'pfmet')
      bookCustomMET( tr, 'nopumet')
      bookCustomMET( tr, 'tkmet')
      bookCustomMET( tr, 'pumet')
      bookCustomMET( tr, 'pucmet')
      bookCustomMET( tr, 'pfMetForRegression')
      bookCustomMET( tr, 'pfmetraw')

      # var( tr, 'pfmetcov00')
      # var( tr, 'pfmetcov01')
      # var( tr, 'pfmetcov10')
      # var( tr, 'pfmetcov11')

      bookW( tr, 'W')
      var( tr, 'W_mt')
      if (self.cfg_comp.isMC):
        bookZ( tr, 'WGen')
        var( tr, 'WGen_mt')
        bookFourVector( tr, 'NuGen')        
          
      # var( tr, 'u1')
      # var( tr, 'u2')

      bookMuon(tr, 'Mu')
      var(tr, 'Mu_dxy')
      var(tr, 'Mu_dz')
      var(tr, 'MuIsTightAndIso', int)
      var(tr, 'MuIsTight', int)
      var(tr, 'pt_vis')
      var(tr, 'phi_vis')
      if (self.cfg_comp.isMC):
        bookParticle(tr, 'MuGen')
        bookParticle(tr, 'MuGenStatus1')
        var(tr, 'MuDRGenP')
        bookParticle(tr, 'NuGen')
        var(tr, 'FSRWeight')
        if (hasattr(self.cfg_ana,'storeLHE_weight') and self.cfg_ana.storeLHE_weight):
          # print "booking tree"
          bookLHE_weight(tr,'LHE' )
    

      
      bookMuonCovMatrix(tr,'Mu' )

      bookJet(tr, 'Jet_leading')
      
      if (self.cfg_comp.isMC):
        var(tr, 'genWLept')
       
    def process(self, iEvent, event):
        
        self.readCollections( iEvent )
        tr = self.tree
        tr.reset()

        if (self.cfg_comp.isMC):
          fill(tr, 'genWLept', len(event.genWLept))

        if (event.savegenpW and self.cfg_comp.isMC):
          
          fill(tr, 'FSRWeight',event.fsrWeight)
          fillZ(tr,'WGen', event.genW[0].p4())
          fill(tr, 'WGen_mt', event.genW_mt)
          fillParticle(tr, 'MuGen',event.genMu[0])
          fillParticle(tr, 'MuGenStatus1', event.genMuStatus1[0])      
          fill(tr, 'MuDRGenP',event.muGenDeltaRgenP)
          fillFourVector(tr, 'NuGen', event.genNu_p4)
          
          if (hasattr(self.cfg_ana,'storeLHE_weight') and self.cfg_ana.storeLHE_weight):
            # print "filling tree"
            fillLHE_weight( tr,'LHE' ,event.LHE_weights ,event)
              

        if event.WGoodEvent == True :
                      
          fillW( tr, 'W',event.W4V)
          fill(tr, 'W_mt', event.W4V_mt)
          # fill(tr, 'u1', event.u1)
          # fill(tr, 'u2', event.u2)

          fillMuon(tr, 'Mu', event.selMuons[0])
          if ( event.selMuons[0].isGlobalMuon() or event.selMuons[0].isTrackerMuon() ) and event.passedVertexAnalyzer:
            fill(tr, 'Mu_dxy', math.fabs(event.selMuons[0].dxy()))
            fill(tr, 'Mu_dz', math.fabs(event.selMuons[0].dz()))
          fill(tr, 'MuIsTightAndIso', event.selMuonIsTightAndIso)
          fill(tr, 'MuIsTight', event.selMuonIsTight)
          fill(tr, 'pt_vis', event.selMuons[0].pt())
          fill(tr, 'phi_vis', event.selMuons[0].phi())
          
          fillMuonCovMatrix( tr,'Mu' ,event.covMatrixMuon ,event)

                    
        if (event.savegenpW and self.cfg_comp.isMC) or event.WGoodEvent:
          fill( tr, 'run', event.run) 
          fill( tr, 'lumi',event.lumi)
          fill( tr, 'evt', event.eventId)
          fill( tr, 'nvtx', len(self.handles['vertices'].product()))          
          fill( tr, 'njets', len(event.selJets))
          
          if (self.cfg_comp.isMC) :

            event.pileUpInfo = map( PileUpSummaryInfo,
                                    self.mchandles['pusi'].product() )
            for puInfo in event.pileUpInfo:
              if puInfo.getBunchCrossing()==0:
                fill( tr, 'npu', puInfo.nTrueInteractions())
                # print 'puInfo.nTrueInteractions()= ',puInfo.nTrueInteractions()
              # else:
                # print 'NO INFO FOR puInfo.getBunchCrossing()==0 !!!!'
          if (self.cfg_comp.isMC) :
              event.generator = self.mchandles['generator'].product()
              # print 'WTreeProducer.py: ',event.generator.pdf().scalePDF,' ',event.generator.pdf().id.first,' ',event.generator.pdf().x.first,' ',event.generator.pdf().id.second,' ',event.generator.pdf().x.second
              fill(tr, 'scalePDF',float(event.generator.pdf().scalePDF))
              fill(tr, 'parton1_pdgId',float(event.generator.pdf().id.first))
              fill(tr, 'parton1_x',float(event.generator.pdf().x.first))
              fill(tr, 'parton2_pdgId',float(event.generator.pdf().id.second))
              fill(tr, 'parton2_x',float(event.generator.pdf().x.second))

          fill( tr, 'nMuons', event.nMuons)
          fill( tr, 'nTrgMuons', len(event.selMuons))
          # if len(event.selMuons): print 'len(event.selMuons) ?!?!?'
          if len(event.NoTriggeredMuonsLeadingPt) > 0 :
            fill( tr, 'noTrgMuonsLeadingPt', event.NoTriggeredMuonsLeadingPt[0].pt())
          fill( tr, 'evtHasGoodVtx', event.passedVertexAnalyzer)
          fill( tr, 'Vtx_ndof', event.goodVertices[0].ndof())
          # fill( tr, 'firstVtxIsGood', event.firstVtxIsGoodVertices) # REQUIRES DEFINITION IN CMGTools/RootTools/python/analyzers/VertexAnalyzer.py
          # fill( tr, 'evtHasTrg', event.passedTriggerAnalyzer)
          fill( tr, 'evtHasTrg', True)
          fill( tr, 'evtWSel', event.WGoodEvent)
          fillCustomMET(tr, 'pfmet', event.pfmet)
          pfMetSignificance = self.handles['pfMetSignificance'].product().significance()
          # fill( tr, 'pfmetcov00', pfMetSignificance(0,0))
          # fill( tr, 'pfmetcov01', pfMetSignificance(0,1))
          # fill( tr, 'pfmetcov10', pfMetSignificance(1,0))
          # fill( tr, 'pfmetcov11', pfMetSignificance(1,1))

          event.pfmetraw = self.handles['pfMetraw'].product()[0]
          event.nopumet = self.handles['nopuMet'].product()[0]
          event.pucmet = self.handles['pucMet'].product()[0]
          event.pfMetForRegression = self.handles['pfMetForRegression'].product()[0]
          event.pumet = self.handles['puMet'].product()[0]
          event.tkmet = self.handles['tkMet'].product()[0]
          fillCustomMET(tr, 'nopumet', event.nopumet)
          fillCustomMET(tr, 'tkmet', event.tkmet)
          fillCustomMET(tr, 'pucmet', event.pucmet)
          fillCustomMET(tr, 'pumet', event.pumet)
          fillCustomMET(tr, 'pfMetForRegression', event.pfMetForRegression)
          fillCustomMET(tr, 'pfmetraw', event.pfmetraw)

          if len(event.selJets)>0:
            fillJet(tr, 'Jet_leading', event.selJets[0])
            
          self.tree.tree.Fill()
       
